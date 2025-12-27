"""
Statistical analysis and reporting module for object detection.
Provides functions for counting objects, generating statistics, and calculating metrics.
"""

import pandas as pd
from typing import Dict, Any, Tuple, Optional


def count_objects(detection_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count objects by class with detailed statistics.
    
    Args:
        detection_df: DataFrame containing detection data with 'class' column
        
    Returns:
        DataFrame with columns: ['class', 'count', 'percentage']
        
    Example:
        >>> df = pd.DataFrame({'class': ['person', 'person', 'car']})
        >>> result = count_objects(df)
        >>> print(result)
           class  count  percentage
        0  person      2       66.67
        1     car      1       33.33
    """
    # Validate input
    if detection_df.empty or 'class' not in detection_df.columns:
        return pd.DataFrame(columns=['class', 'count', 'percentage'])
    
    try:
        # Count objects per class
        counts = detection_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        
        # Calculate percentages
        total = counts['count'].sum()
        if total > 0:
            counts['percentage'] = (counts['count'] / total * 100).round(2)
        else:
            counts['percentage'] = 0.0
        
        # Sort by count descending
        return counts.sort_values('count', ascending=False)
        
    except Exception as e:
        print(f"Error in count_objects: {e}")
        return pd.DataFrame(columns=['class', 'count', 'percentage'])


def generate_statistics(detection_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate comprehensive detection statistics.
    
    Args:
        detection_df: DataFrame containing detection data
        
    Returns:
        Dictionary containing all calculated statistics
        
    Statistics include:
        - Basic counts (total objects, unique classes)
        - Confidence metrics (mean, std, min, max)
        - Most common class information
        - Size metrics (if available)
    """
    # Return empty stats if no data
    if detection_df.empty:
        return {
            'total_objects': 0,
            'unique_classes': 0,
            'message': 'No objects detected'
        }
    
    try:
        # Initialize statistics dictionary
        stats = {}
        
        # 1. Basic counts
        stats['total_objects'] = int(len(detection_df))
        stats['unique_classes'] = int(detection_df['class'].nunique())
        
        # 2. Confidence statistics
        if 'confidence' in detection_df.columns:
            confidence_series = detection_df['confidence']
            stats.update({
                'confidence_mean': float(round(confidence_series.mean(), 3)),
                'confidence_std': float(round(confidence_series.std(), 3)),
                'confidence_min': float(round(confidence_series.min(), 3)),
                'confidence_max': float(round(confidence_series.max(), 3)),
                'confidence_median': float(round(confidence_series.median(), 3))
            })
        
        # 3. Most common class
        if 'class' in detection_df.columns:
            class_counts = detection_df['class'].value_counts()
            if not class_counts.empty:
                most_common = class_counts.index[0]
                stats.update({
                    'most_common_class': str(most_common),
                    'most_common_count': int(class_counts.iloc[0]),
                    'most_common_percentage': float(round(class_counts.iloc[0] / len(detection_df) * 100, 2))
                })
        
        # 4. Size statistics (if available)
        if all(col in detection_df.columns for col in ['width', 'height', 'area']):
            stats.update({
                'total_area': float(round(detection_df['area'].sum(), 2)),
                'avg_area': float(round(detection_df['area'].mean(), 2)),
                'avg_width': float(round(detection_df['width'].mean(), 2)),
                'avg_height': float(round(detection_df['height'].mean(), 2))
            })
            
            # Find largest and smallest objects
            if not detection_df.empty:
                largest_idx = detection_df['area'].idxmax()
                smallest_idx = detection_df['area'].idxmin()
                
                stats.update({
                    'largest_object_class': str(detection_df.loc[largest_idx, 'class']),
                    'largest_object_area': float(round(detection_df.loc[largest_idx, 'area'], 2)),
                    'smallest_object_class': str(detection_df.loc[smallest_idx, 'class']),
                    'smallest_object_area': float(round(detection_df.loc[smallest_idx, 'area'], 2))
                })
        
        return stats
        
    except Exception as e:
        print(f"Error in generate_statistics: {e}")
        return {
            'total_objects': len(detection_df),
            'unique_classes': detection_df['class'].nunique() if 'class' in detection_df.columns else 0,
            'error': str(e)
        }


def calculate_metrics(detection_df: pd.DataFrame, image_size: Tuple[int, int]) -> Dict[str, float]:
    """
    Calculate advanced detection metrics based on image size.
    
    Args:
        detection_df: DataFrame containing detection data
        image_size: Tuple containing (width, height) of original image in pixels
        
    Returns:
        Dictionary containing calculated metrics:
            - coverage_percentage: Percentage of image covered by detections
            - avg_aspect_ratio: Average width/height ratio of detections
            - density: Objects per 10,000 pixels
    """
    # Return empty dict if no data or missing columns
    if detection_df.empty or 'area' not in detection_df.columns:
        return {}
    
    try:
        img_width, img_height = image_size
        image_area = img_width * img_height
        
        # Guard against zero area
        if image_area == 0:
            return {}
        
        # 1. Calculate coverage percentage
        total_detection_area = detection_df['area'].sum()
        coverage_percentage = (total_detection_area / image_area) * 100
        
        # 2. Calculate average aspect ratio (width/height)
        avg_aspect_ratio = 0.0
        if all(col in detection_df.columns for col in ['width', 'height']):
            # Filter out zero heights to avoid division by zero
            valid_rows = detection_df['height'] > 0
            if valid_rows.any():
                aspect_ratios = detection_df.loc[valid_rows, 'width'] / detection_df.loc[valid_rows, 'height']
                avg_aspect_ratio = aspect_ratios.mean()
        
        # 3. Calculate density (objects per 10,000 pixels)
        density = (len(detection_df) / image_area) * 10000
        
        # Create metrics dictionary with rounded values
        metrics = {
            'coverage_percentage': round(coverage_percentage, 2),
            'avg_aspect_ratio': round(avg_aspect_ratio, 3),
            'density': round(density, 3)
        }
        
        return metrics
        
    except Exception as e:
        print(f"Error in calculate_metrics: {e}")
        return {}


def format_statistics(stats: Dict[str, Any]) -> str:
    """
    Format statistics dictionary into a readable text report.
    
    Args:
        stats: Statistics dictionary from generate_statistics()
        
    Returns:
        Formatted string report suitable for display or export
        
    Example:
        >>> stats = {'total_objects': 5, 'unique_classes': 3}
        >>> print(format_statistics(stats))
        DETECTION STATISTICS
        ====================
        Total Objects: 5
        Unique Classes: 3
    """
    if not stats or 'message' in stats:
        return stats.get('message', 'No statistics available')
    
    try:
        lines = ["DETECTION STATISTICS", "=" * 40]
        
        # Group statistics by category
        categories = {
            'Counts': ['total_objects', 'unique_classes'],
            'Confidence': ['confidence_mean', 'confidence_std', 'confidence_min', 
                          'confidence_max', 'confidence_median'],
            'Most Common': ['most_common_class', 'most_common_count', 'most_common_percentage'],
            'Size Metrics': ['total_area', 'avg_area', 'avg_width', 'avg_height',
                            'largest_object_class', 'largest_object_area',
                            'smallest_object_class', 'smallest_object_area']
        }
        
        # Add statistics by category
        for category, keys in categories.items():
            # Check if any key in this category exists in stats
            existing_keys = [k for k in keys if k in stats]
            if existing_keys:
                lines.append(f"\n{category.upper()}")
                lines.append("-" * 30)
                
                for key in existing_keys:
                    # Format key for display
                    display_key = key.replace('_', ' ').title()
                    value = stats[key]
                    
                    # Format value based on type
                    if 'percentage' in key or 'confidence' in key:
                        lines.append(f"{display_key}: {value:.2f}%")
                    elif 'area' in key or 'width' in key or 'height' in key:
                        lines.append(f"{display_key}: {value:.2f} px²")
                    elif 'mean' in key or 'std' in key or 'median' in key:
                        lines.append(f"{display_key}: {value:.3f}")
                    else:
                        lines.append(f"{display_key}: {value}")
        
        return "\n".join(lines)
        
    except Exception as e:
        print(f"Error in format_statistics: {e}")
        return f"Error formatting statistics: {str(e)}"


def validate_detection_data(detection_df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate detection DataFrame structure and content.
    
    Args:
        detection_df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if detection_df.empty:
        return False, "Empty detection data"
    
    required_columns = ['class', 'confidence']
    missing_columns = [col for col in required_columns if col not in detection_df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for invalid confidence values
    if 'confidence' in detection_df.columns:
        invalid_confidences = detection_df['confidence'][
            (detection_df['confidence'] < 0) | (detection_df['confidence'] > 1)
        ]
        if not invalid_confidences.empty:
            return False, f"Invalid confidence values found: {len(invalid_confidences)}"
    
    return True, "Data validation successful"


def get_summary_report(detection_df: pd.DataFrame, image_size: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
    """
    Generate a complete summary report including all statistics and metrics.
    
    Args:
        detection_df: DataFrame containing detection data
        image_size: Optional image size for metrics calculation
        
    Returns:
        Dictionary containing complete report with:
            - validation: Data validation results
            - statistics: Basic statistics
            - metrics: Advanced metrics (if image_size provided)
            - distribution: Class distribution
            - formatted: Formatted text report
    """
    report = {}
    
    # 1. Data validation
    is_valid, validation_msg = validate_detection_data(detection_df)
    report['validation'] = {
        'is_valid': is_valid,
        'message': validation_msg
    }
    
    if not is_valid:
        return report
    
    # 2. Basic statistics
    report['statistics'] = generate_statistics(detection_df)
    
    # 3. Advanced metrics (if image size provided)
    if image_size:
        report['metrics'] = calculate_metrics(detection_df, image_size)
    
    # 4. Class distribution
    report['distribution'] = count_objects(detection_df).to_dict('records')
    
    # 5. Formatted report
    report['formatted'] = format_statistics(report['statistics'])
    
    return report