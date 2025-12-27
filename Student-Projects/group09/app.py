"""
Main Streamlit application for YOLOv8 Object Detection.

"""

import streamlit as st
import pandas as pd
from PIL import Image
import tempfile
import os
from typing import Optional, Tuple
import traceback

from utils.detection import ObjectDetector
from utils.counting import (
    count_objects, 
    generate_statistics, 
    format_statistics, 
    calculate_metrics,
    get_summary_report
)


# ==================== CONSTANTS ====================
SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png']
MODEL_OPTIONS = {
    'YOLOv8 Nano (Fastest)': 'yolov8n.pt',
    'YOLOv8 Small (Balanced)': 'yolov8s.pt',
    'YOLOv8 Medium (Accurate)': 'yolov8m.pt'
}
APP_TITLE = "Object Detection System - YOLOv8"
APP_VERSION = "1.0.0"


# ==================== PAGE CONFIGURATION ====================
def setup_page_configuration() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🔍",
        menu_items={
            'Get Help': 'https://github.com/ultralytics/yolov8',
            'Report a bug': 'https://github.com/ultralytics/yolov8/issues',
            'About': f"""
            # {APP_TITLE}
            
            **Version:** {APP_VERSION}
            
            A professional object detection system using YOLOv8.
            
            Features:
            - Real-time object detection
            - Multiple model options
            - Detailed statistics and analytics
            - Data export capabilities
            """
        }
    )


# ==================== SIDEBAR COMPONENTS ====================
def create_sidebar() -> Tuple[str, Optional[st.runtime.uploaded_file_manager.UploadedFile]]:
    """
    Create and render the sidebar with user controls.
    
    Returns:
        Tuple of (selected_model_name, uploaded_file)
    """
    with st.sidebar:
        # Header
        st.title("⚙️ Configuration Panel")
        st.markdown("---")
        
        # Model Selection
        st.subheader("Model Selection")
        model_display_name = st.selectbox(
            "Choose Detection Model",
            list(MODEL_OPTIONS.keys()),
            index=0,
            help="""Nano: Fastest, suitable for real-time applications.
            Small: Balanced speed and accuracy.
            Medium: Highest accuracy, slower processing."""
        )
        selected_model = MODEL_OPTIONS[model_display_name]
        
        st.markdown("---")
        
        # File Upload
        st.subheader("Image Upload")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=SUPPORTED_FORMATS,
            help=f"Supported formats: {', '.join(SUPPORTED_FORMATS).upper()}",
            key="file_uploader"
        )
        
        # Information Panel
        with st.expander("📚 Quick Guide", expanded=False):
            st.markdown("""
            ### How to Use:
            1. **Upload** an image using the file uploader
            2. **Select** a model based on your needs
            3. **View** detection results and statistics
            4. **Export** data for further analysis
            
            ### Tips:
            - Use JPG/PNG format for best results
            - For real-time needs, choose Nano model
            - For accuracy, choose Medium model
            """)
        
        st.markdown("---")
        st.caption(f"Version {APP_VERSION}")
    
    return selected_model, uploaded_file


# ==================== IMAGE PROCESSING ====================
def process_image_file(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
    model_name: str
) -> Tuple[Optional[Image.Image], Optional[pd.DataFrame], Optional[str]]:
    """
    Process uploaded image file through object detection pipeline.
    
    Args:
        uploaded_file: Uploaded file object from Streamlit
        model_name: Name of YOLO model to use
        
    Returns:
        Tuple of (processed_image, detection_dataframe, error_message)
    """
    temp_file_path = None
    
    try:
        # Validate input
        if uploaded_file is None:
            return None, None, "No file uploaded"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        
        # Initialize detector
        detector = ObjectDetector(model_name)
        
        # Perform object detection
        processed_image_array = detector.detect_objects(temp_file_path)
        
        # Convert numpy array to PIL Image
        processed_image = Image.fromarray(processed_image_array)
        
        # Get detection data
        detection_df = detector.get_detection_data()
        
        return processed_image, detection_df, None
        
    except FileNotFoundError as e:
        return None, None, f"File error: {str(e)}"
    except RuntimeError as e:
        return None, None, f"Detection error: {str(e)}"
    except Exception as e:
        return None, None, f"Unexpected error: {str(e)}"
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass


# ==================== RESULT DISPLAY ====================
def display_image_comparison(
    original_image: Image.Image,
    processed_image: Image.Image
) -> None:
    """
    Display original and processed images side by side.
    
    Args:
        original_image: Original uploaded image
        processed_image: Processed image with detections
    """
    st.subheader("🖼️ Image Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Original Image")
        st.image(
            original_image,
            use_container_width=True,
            caption=f"Dimensions: {original_image.size[0]} × {original_image.size[1]} pixels"
        )
    
    with col2:
        st.markdown("### Processed Image")
        st.image(
            processed_image,
            use_container_width=True,
            caption="With object detection bounding boxes"
        )
    
    st.markdown("---")


def display_detection_details(detection_df: pd.DataFrame) -> None:
    """
    Display detailed detection data in a table.
    
    Args:
        detection_df: DataFrame containing detection results
    """
    if detection_df.empty:
        st.warning("No objects detected in the image.")
        return
    
    st.subheader("📊 Detection Details")
    
    # Display data table with formatting
    st.dataframe(
        detection_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "confidence": st.column_config.ProgressColumn(
                "Confidence",
                help="Detection confidence score (0-1)",
                format="%.3f",
                min_value=0,
                max_value=1,
            ),
            "class": st.column_config.TextColumn(
                "Class",
                help="Detected object class"
            ),
            "area": st.column_config.NumberColumn(
                "Area",
                help="Bounding box area in pixels²",
                format="%.0f"
            )
        }
    )


def display_statistics_panel(
    detection_df: pd.DataFrame,
    image_size: Tuple[int, int],
    processed_image: Image.Image
) -> None:
    """
    Display comprehensive statistics and metrics.
    
    Args:
        detection_df: DataFrame containing detection results
        image_size: Original image dimensions
        processed_image: Processed image for export
    """
    if detection_df.empty:
        return
    
    # Create tabs for organized display
    tab1, tab2, tab3 = st.tabs(["📈 Statistics", "📋 Distribution", "💾 Export"])
    
    with tab1:
        display_statistics_tab(detection_df, image_size)
    
    with tab2:
        display_distribution_tab(detection_df)
    
    with tab3:
        display_export_tab(detection_df, processed_image)


def display_statistics_tab(detection_df: pd.DataFrame, image_size: Tuple[int, int]) -> None:
    """Display statistics in the statistics tab."""
    # Generate statistics
    stats = generate_statistics(detection_df)
    metrics = calculate_metrics(detection_df, image_size)
    
    # Key metrics in columns
    st.subheader("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Objects", stats.get('total_objects', 0))
    
    with col2:
        st.metric("Unique Classes", stats.get('unique_classes', 0))
    
    with col3:
        conf_mean = stats.get('confidence_mean', 0)
        st.metric("Avg Confidence", f"{conf_mean:.1%}")
    
    with col4:
        coverage = metrics.get('coverage_percentage', 0)
        st.metric("Image Coverage", f"{coverage:.1f}%")
    
    # Detailed statistics
    with st.expander("View Detailed Statistics", expanded=False):
        formatted_stats = format_statistics(stats)
        st.text_area("Complete Statistics", formatted_stats, height=200)
        
        # Display metrics if available
        if metrics:
            st.markdown("#### Advanced Metrics")
            for key, value in metrics.items():
                display_name = key.replace('_', ' ').title()
                st.write(f"**{display_name}:** {value}")


def display_distribution_tab(detection_df: pd.DataFrame) -> None:
    """Display class distribution in the distribution tab."""
    distribution_df = count_objects(detection_df)
    
    if not distribution_df.empty:
        # Display as table
        st.dataframe(
            distribution_df,
            use_container_width=True,
            column_config={
                "percentage": st.column_config.NumberColumn(
                    "Percentage",
                    format="%.2f%%"
                )
            }
        )
        
        # Create simple bar chart using Streamlit native
        chart_data = distribution_df.set_index('class')['count']
        st.bar_chart(chart_data)


def display_export_tab(detection_df: pd.DataFrame, processed_image: Image.Image) -> None:
    """Display export options in the export tab."""
    st.subheader("Export Results")
    
    # Create export buttons in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export processed image
        try:
            processed_image.save("temp_processed_image.jpg")
            with open("temp_processed_image.jpg", "rb") as img_file:
                img_data = img_file.read()
            
            st.download_button(
                label="📷 Download Image",
                data=img_data,
                file_name="detection_result.jpg",
                mime="image/jpeg",
                help="Download image with bounding boxes",
                key="download_image"
            )
            
            # Cleanup
            if os.path.exists("temp_processed_image.jpg"):
                os.remove("temp_processed_image.jpg")
                
        except Exception as e:
            st.error(f"Error preparing image download: {str(e)}")
    
    with col2:
        # Export CSV data
        try:
            csv_data = detection_df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name="detection_data.csv",
                mime="text/csv",
                help="Download detection data as CSV file",
                key="download_csv"
            )
        except Exception as e:
            st.error(f"Error preparing CSV: {str(e)}")
    
    with col3:
        # Export statistics report
        try:
            stats = generate_statistics(detection_df)
            report_text = format_statistics(stats)
            
            st.download_button(
                label="📊 Download Report",
                data=report_text,
                file_name="detection_report.txt",
                mime="text/plain",
                help="Download detailed statistics report",
                key="download_report"
            )
        except Exception as e:
            st.error(f"Error preparing report: {str(e)}")


# ==================== WELCOME SCREEN ====================
def display_welcome_screen() -> None:
    """Display welcome screen when no image is uploaded."""
    st.title("🎯 Object Detection System")
    st.markdown(f"### Version {APP_VERSION}")
    st.markdown("---")
    
    # Welcome message
    st.info(
        """
        👈 **Upload an image from the sidebar to begin detection**
        
        This system uses YOLOv8 (You Only Look Once version 8) for real-time 
        object detection. Upload any image to detect and analyze objects.
        """,
        icon="ℹ️"
    )
    
    # Feature highlights
    st.subheader("✨ Key Features")
    
    features = [
        ("🚀 Real-time Detection", "Fast object detection using YOLOv8 architecture"),
        ("🎯 High Accuracy", "Detects 80+ object classes with precise bounding boxes"),
        ("📊 Comprehensive Analytics", "Detailed statistics, metrics, and visualizations"),
        ("💾 Multiple Export Options", "Export images, CSV data, and reports"),
        ("⚙️ Flexible Configuration", "Choose between different model sizes"),
        ("📱 Responsive Interface", "Clean, modern web interface")
    ]
    
    # Display features in columns
    cols = st.columns(3)
    for idx, (title, description) in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"**{title}**")
            st.markdown(description)
            st.markdown("---")
    
    # Quick start guide
    with st.expander("📖 Getting Started Guide", expanded=True):
        st.markdown("""
        ### Quick Start:
        
        1. **Upload Image**: Click 'Browse files' in the sidebar
        2. **Select Model**: Choose based on speed/accuracy needs
        3. **View Results**: See detections and detailed statistics
        4. **Export Data**: Download results for analysis or reporting
        
        ### Supported Formats:
        - JPEG/JPG (Recommended)
        - PNG (Transparency supported)
        
        ### Model Options:
        - **Nano**: Fastest, suitable for real-time applications
        - **Small**: Balanced speed and accuracy
        - **Medium**: Highest accuracy, ideal for detailed analysis
        """)
    
    st.markdown("---")
    st.caption("Built with Streamlit, YOLOv8, and OpenCV")


# ==================== ERROR HANDLING ====================
def display_error_message(error_msg: str, details: str = "") -> None:
    """
    Display error message to user.
    
    Args:
        error_msg: User-friendly error message
        details: Technical details for debugging
    """
    st.error(f"❌ **Error**: {error_msg}")
    
    if details and st.checkbox("Show technical details"):
        with st.expander("Technical Details"):
            st.code(details)


# ==================== MAIN APPLICATION ====================
def main() -> None:
    """Main application entry point."""
    try:
        # Setup page configuration
        setup_page_configuration()
        
        # Create sidebar and get user inputs
        selected_model, uploaded_file = create_sidebar()
        
        # Check if file is uploaded
        if uploaded_file is not None:
            # Display processing status
            with st.spinner("Processing image..."):
                # Load original image
                original_image = Image.open(uploaded_file)
                image_size = original_image.size
                
                # Process image through detection pipeline
                processed_image, detection_df, error_msg = process_image_file(
                    uploaded_file, 
                    selected_model
                )
                
                # Check for processing errors
                if error_msg:
                    display_error_message(error_msg)
                    return
                
                # Display results
                if processed_image is not None and detection_df is not None:
                    # Display image comparison
                    display_image_comparison(original_image, processed_image)
                    
                    # Display detection details
                    display_detection_details(detection_df)
                    
                    # Display statistics and export options
                    if not detection_df.empty:
                        display_statistics_panel(
                            detection_df, 
                            image_size, 
                            processed_image
                        )
        
        else:
            # No file uploaded - show welcome screen
            display_welcome_screen()
            
    except Exception as e:
        # Catch any unexpected errors
        error_details = traceback.format_exc()
        display_error_message(
            "An unexpected error occurred in the application.",
            error_details
        )


# ==================== APPLICATION ENTRY POINT ====================
if __name__ == "__main__":
    main()