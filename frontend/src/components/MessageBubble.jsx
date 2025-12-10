import React from 'react'
import { Bot, User, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { format } from 'date-fns'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const sentiment = message.sentiment

  // Agent color mapping
  const agentColors = {
    master: 'bg-blue-100 text-blue-800',
    engage: 'bg-green-100 text-green-800',
    verify: 'bg-purple-100 text-purple-800',
    underwrite: 'bg-orange-100 text-orange-800',
    sanction: 'bg-indigo-100 text-indigo-800',
    system: 'bg-gray-100 text-gray-800',
  }

  const getSentimentIcon = () => {
    if (!sentiment) return null
    
    if (sentiment.sentiment === 'positive') {
      return <TrendingUp className="w-4 h-4 text-green-500" />
    } else if (sentiment.sentiment === 'negative') {
      return <TrendingDown className="w-4 h-4 text-red-500" />
    }
    return <Minus className="w-4 h-4 text-gray-500" />
  }

  return (
    <div className={`flex items-start space-x-2 animate-fade-in ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
        isUser ? 'bg-primary-600' : agentColors[message.agent] || 'bg-gray-200'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Agent Badge */}
        {!isUser && message.agent && (
          <div className="flex items-center space-x-2 mb-1">
            <span className={`text-xs px-2 py-1 rounded-full ${agentColors[message.agent]}`}>
              {message.agent.charAt(0).toUpperCase() + message.agent.slice(1)} Agent
            </span>
            {sentiment && (
              <div className="flex items-center space-x-1">
                {getSentimentIcon()}
              </div>
            )}
          </div>
        )}

        {/* Message Bubble */}
        <div className={`p-3 rounded-lg ${
          isUser 
            ? 'bg-primary-600 text-white' 
            : message.error 
            ? 'bg-red-50 text-red-900 border border-red-200'
            : 'bg-gray-100 text-gray-900'
        }`}>
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Timestamp */}
        <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {format(new Date(message.timestamp), 'HH:mm')}
        </div>
      </div>
    </div>
  )
}


