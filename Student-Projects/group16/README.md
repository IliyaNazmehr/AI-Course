# Group 16 
# 🐦 Tweet Generator - AI-Powered Chatbot - developed by Turing Gang Gp

A modern, fast, and user-friendly React application that generates engaging, viral-style tweets in Persian (Farsi) and English using Google's Gemini AI. Transform your ideas into compelling social media content with intelligent language detection and automatic formatting.

## ✨ Features

- **🤖 AI-Powered Generation**: Uses Google Gemini 2.5 Flash model for intelligent tweet generation
- **🌐 Bilingual Support**: Automatically detects and generates tweets in Persian (Farsi) or English based on input
- **📏 Character Limit Compliance**: Ensures all tweets stay within Twitter's 280-character limit
- **🔥 Viral-Style Content**: Creates engaging tweets with compelling hooks, natural tone, and trending hashtags
- **📋 One-Click Copy**: Click on any bot-generated tweet to instantly copy it to clipboard
- **⚡ Real-Time Chat Interface**: Smooth, responsive chat experience with auto-scrolling
- **🎨 Modern UI/UX**: Clean, intuitive interface with Persian language support
- **🛡️ Error Handling**: Comprehensive error handling with user-friendly Persian error messages
- **🔒 Privacy-Focused**: No data storage - all processing happens client-side with API calls
- **🔧 Highly Flexible**: Easily customizable prompt system - adapt the chatbot for any use case by modifying the prompt template (content writing, business, education, creative writing, and more)

## Members

- **Mohammad Amin Kavousi** (40110130117116)
- **Ahoora Shariat jafari** (40110130117237)


## 📸 Screenshots

### Main Interface

![Application Screenshot 1](./docs/img1.png)

### Chat Interface with Generated Tweet

![Application Screenshot 2](./docs/img2.png)

### Mobile

![Application Screenshot 2](./docs/img3.png)

## 🚀 Technologies & Stack

### Core Framework

- **React 18.3.1** - Modern UI library with hooks and functional components
- **Vite 6.0.1** - Lightning-fast build tool and development server
- **ES Modules** - Modern JavaScript module system

### AI & APIs

- **@google/genai 1.26.0** - Official Google Generative AI SDK
- **Gemini 2.5 Flash** - Fast and efficient AI model for content generation

### Development Tools

- **ESLint 9.15.0** - Code quality and consistency
- **React Hooks Plugin** - Enforces React hooks best practices
- **TypeScript Types** - Type definitions for better IDE support

### Styling

- **CSS Modules** - Component-scoped styling
- **CSS Custom Properties** - Consistent design system with CSS variables
- **Responsive Design** - Mobile-first approach with media queries

## 📁 Project Structure

```
chatbot-proj/
├── src/
│   ├── components/          # React components
│   │   ├── ChatInput.jsx    # Message input with API integration
│   │   ├── ChatMessage.jsx  # Individual message display with copy feature
│   │   ├── ChatMessages.jsx # Message list container with auto-scroll
│   │   ├── ErrorPopup.jsx   # Error notification modal
│   │   └── WelcomeMessage.jsx # Welcome screen with features
│   ├── hooks/               # Custom React hooks
│   │   └── useApiKey.js     # API key management with memoization
│   ├── utils/               # Utility functions
│   │   └── errorHandler.js  # Error message translation
│   ├── config/              # Configuration
│   │   └── env.js           # Environment variable management
│   ├── prompts/             # AI prompts
│   │   └── tweetPrompt.js   # Specialized tweet generation prompt
│   ├── assets/              # Static assets
│   │   ├── bot.png          # Bot avatar
│   │   └── user.png         # User avatar
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # Application entry point
│   └── index.css            # Global styles and CSS variables
├── public/                  # Static public assets
├── .env.example             # Environment variables template
├── vite.config.js           # Vite configuration
├── eslint.config.js         # ESLint configuration
└── package.json             # Dependencies and scripts
```

## 🏗️ Architecture & Best Practices

### 1. **Component-Based Architecture**

- ✅ Modular, reusable components with single responsibility
- ✅ Separation of concerns (UI, logic, data)
- ✅ Functional components with React Hooks
- ✅ Proper component composition

### 2. **State Management**

- ✅ Local state with `useState` for component-specific data
- ✅ Lifted state for shared data (messages in App component)
- ✅ Optimistic UI updates for better UX
- ✅ Proper state cleanup and error rollback

### 3. **Performance Optimizations**

- ✅ **React.memo** potential (components are optimized for re-renders)
- ✅ **useMemo** for API key caching (`useApiKey` hook)
- ✅ **useRef** for DOM manipulation (scroll container)
- ✅ **useEffect** with proper dependencies for side effects
- ✅ **Crypto.randomUUID()** for efficient unique ID generation
- ✅ **Vite** for fast HMR and optimized production builds

### 4. **Code Quality**

- ✅ **ESLint** configuration with React best practices
- ✅ **Strict Mode** enabled for development warnings
- ✅ **JSDoc comments** for function documentation
- ✅ **Consistent naming conventions** (camelCase for variables, PascalCase for components)
- ✅ **Error boundaries** through try-catch blocks

### 5. **User Experience**

- ✅ **Loading states** to prevent duplicate submissions
- ✅ **Disabled states** during API calls
- ✅ **Auto-scrolling** to latest messages
- ✅ **Keyboard shortcuts** (Enter to send)
- ✅ **Visual feedback** (copy notifications, loading indicators)
- ✅ **Auto-closing error popups** (5-second timer)
- ✅ **Click-outside-to-close** for modals

### 6. **Error Handling**

- ✅ **Centralized error handler** (`errorHandler.js`)
- ✅ **User-friendly Persian error messages**
- ✅ **Error categorization** (network, API, quota, timeout)
- ✅ **Graceful error recovery** (rollback on failure)
- ✅ **Error popup component** for non-intrusive notifications

### 7. **Security & Privacy**

- ✅ **Environment variables** for sensitive data (API keys)
- ✅ **No data persistence** - client-side only
- ✅ **Input validation** (trim, empty check)
- ✅ **Secure API key handling** through config module
- ✅ **.gitignore** properly configured to exclude sensitive files

### 8. **Styling Best Practices**

- ✅ **CSS Custom Properties** for theming and consistency
- ✅ **Component-scoped CSS** files
- ✅ **Responsive design** with mobile-first approach
- ✅ **Semantic HTML** with proper accessibility attributes
- ✅ **Modern CSS** (Flexbox, CSS Grid where appropriate)

### 9. **API Integration**

- ✅ **Async/await** for clean asynchronous code
- ✅ **Proper error handling** in API calls
- ✅ **Request validation** before API calls
- ✅ **Response validation** (checking for valid response structure)

### 10. **Development Experience**

- ✅ **Fast HMR** with Vite
- ✅ **ESLint** for code quality
- ✅ **Clear project structure**
- ✅ **Environment-based configuration**

## ⚡ Performance Characteristics

### Build & Development

- **Vite**: Ultra-fast development server with instant HMR
- **ES Modules**: Native browser module support, no bundling overhead in dev
- **Optimized Production Builds**: Tree-shaking and minification via Vite

### Runtime Performance

- **Lightweight Bundle**: Minimal dependencies, optimized bundle size
- **Efficient Re-renders**: Proper React patterns prevent unnecessary renders
- **Fast API Calls**: Direct integration with Google Gemini API
- **Optimized State Updates**: Batched updates and proper dependency arrays
- **Memory Efficient**: No data persistence, minimal memory footprint

### User Experience Performance

- **Instant UI Feedback**: Optimistic updates show messages immediately
- **Smooth Scrolling**: Native browser scrolling with auto-scroll to bottom
- **Fast Copy Operations**: Native Clipboard API for instant copying
- **Responsive Design**: Works seamlessly on mobile and desktop

### API Performance

- **Gemini 2.5 Flash**: Fast inference model optimized for speed
- **Efficient Prompts**: Concise, well-structured prompts for faster responses
- **Error Recovery**: Quick error handling without blocking UI

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Google Gemini API key

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd chatbot-proj
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Add your Google API key:

   ```
   VITE_GOOGLE_API_KEY=your_api_key_here
   ```

4. **Start development server**

   ```bash
   npm run dev
   ```

5. **Build for production**

   ```bash
   npm run build
   ```

6. **Preview production build**
   ```bash
   npm run preview
   ```

## 📝 Available Scripts

- `npm run dev` - Start development server with HMR
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint to check code quality

## 🔧 Configuration

### Environment Variables

- `VITE_GOOGLE_API_KEY` - Your Google Gemini API key (required)

### Vite Configuration

- React plugin enabled for JSX support
- Optimized for modern browsers
- Fast refresh enabled for development

### ESLint Configuration

- React recommended rules
- React Hooks rules
- Modern ES2020+ syntax support
- JSX runtime enabled

## 🎯 Usage

1. Enter your topic or text in the input field
2. Press Enter or click "Send"
3. Wait for the AI to generate your tweet
4. Click on the generated tweet to copy it to clipboard
5. Share your tweet on social media!

## 🌟 Key Features Explained

### Intelligent Language Detection

The AI automatically detects whether your input is in Persian or English and generates the tweet in the appropriate language, maintaining cultural context and natural phrasing.

### Viral-Style Generation

Tweets are crafted with:

- Compelling hooks to grab attention
- Natural, conversational tone
- Relevant trending hashtags
- Proper formatting for readability

### Character Limit Compliance

All generated tweets automatically respect Twitter's 280-character limit, ensuring they're ready to post.

## 🔧 Customization & Flexibility

### Customizing the AI Prompt

This chatbot is highly flexible and can be easily customized for different use cases. The AI behavior is controlled by the prompt template located in `src/prompts/tweetPrompt.js`.

#### How to Customize

1. **Edit the Prompt File**

   - Navigate to `src/prompts/tweetPrompt.js`
   - Modify the `tweetPrompt` constant to change the AI's behavior
   - The prompt defines the AI's role, instructions, and output format

2. **Example Customizations**

   **Change the Output Format:**

   - Modify the prompt to generate LinkedIn posts, Instagram captions, or blog titles
   - Adjust character limits for different platforms
   - Change the tone (professional, casual, humorous, etc.)

   **Modify Language Behavior:**

   - Change default language preferences
   - Add support for additional languages
   - Adjust language detection logic

   **Alter Content Style:**

   - Change from viral-style to informative or educational
   - Modify hashtag requirements
   - Adjust formatting preferences

3. **Prompt Structure**
   The current prompt includes:
   - **Role Definition**: What the AI should act as
   - **Task Description**: What the bot does
   - **Rules & Constraints**: Guidelines for output
   - **Output Format**: How the response should be structured

#### Use Cases

With prompt customization, this chatbot can be adapted for:

- 📝 **Content Writing**: Blog posts, articles, social media content
- 💼 **Business**: Email templates, product descriptions, marketing copy
- 🎓 **Education**: Study notes, explanations, summaries
- 🎨 **Creative**: Story ideas, poetry, creative writing prompts
- 📊 **Data**: Summaries, reports, analysis explanations
- 🌐 **Multilingual**: Support for any language with proper prompt configuration

#### Best Practices for Prompt Customization

- ✅ Be specific about the desired output format
- ✅ Include examples in your prompt for better results
- ✅ Set clear constraints (length, tone, style)
- ✅ Test different prompt variations to find what works best
- ✅ Keep prompts concise but comprehensive
- ✅ Update the prompt based on your specific use case

The modular architecture makes it easy to swap prompts or create multiple prompt files for different chatbot personalities or use cases.

## 🤝 Contributing

This project follows modern React best practices. When contributing:

- Follow the existing code style
- Use functional components and hooks
- Add proper error handling
- Update documentation as needed
- Test your changes thoroughly

## 🙏 Acknowledgments

- Google Gemini AI for powerful content generation
- React team for the excellent framework
- Vite team for the blazing-fast build tool

---

**Built with ❤️ using React, Vite, and Google Gemini AI**
