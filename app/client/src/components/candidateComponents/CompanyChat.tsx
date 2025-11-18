import { useState } from 'react';
import { Send, Paperclip, Search, MoreVertical } from 'lucide-react';

export default function CompanyChat() {
  const [selectedChat, setSelectedChat] = useState(1);
  const [messageInput, setMessageInput] = useState('');

  const conversations = [
    {
      id: 1,
      company: 'TechCorp Inc.',
      contact: 'Sarah Johnson',
      position: 'HR Manager',
      lastMessage: 'We would love to schedule an interview with you',
      timestamp: '10:30 AM',
      unread: 2,
      logo: '🏢',
    },
    {
      id: 2,
      company: 'StartupXYZ',
      contact: 'Mike Chen',
      position: 'Tech Lead',
      lastMessage: 'Thanks for applying! Looking forward to our call.',
      timestamp: 'Yesterday',
      unread: 0,
      logo: '🚀',
    },
    {
      id: 3,
      company: 'DesignHub',
      contact: 'Emily Rodriguez',
      position: 'Design Director',
      lastMessage: 'Your portfolio looks great!',
      timestamp: '2 days ago',
      unread: 1,
      logo: '🎨',
    },
  ];

  const messages = [
    {
      id: 1,
      sender: 'company',
      content: 'Hi! Thank you for applying to the Senior Frontend Developer position.',
      timestamp: '9:45 AM',
    },
    {
      id: 2,
      sender: 'company',
      content: 'We were really impressed by your portfolio and experience with React and TypeScript.',
      timestamp: '9:46 AM',
    },
    {
      id: 3,
      sender: 'user',
      content: 'Thank you! I\'m very excited about this opportunity. The projects at TechCorp look amazing.',
      timestamp: '9:50 AM',
    },
    {
      id: 4,
      sender: 'company',
      content: 'We would love to schedule an interview with you. Are you available next Tuesday at 2 PM?',
      timestamp: '10:30 AM',
    },
    {
      id: 5,
      sender: 'user',
      content: 'Yes, Tuesday at 2 PM works perfectly for me. Should I prepare anything specific?',
      timestamp: '10:32 AM',
    },
  ];

  const selectedConversation = conversations.find(c => c.id === selectedChat);

  const handleSendMessage = () => {
    if (messageInput.trim()) {
      console.log('Sending message:', messageInput);
      setMessageInput('');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2>Company Chat</h2>
        <p className="text-muted-foreground">Connect with employers and recruiters</p>
      </div>

      <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden h-[calc(100vh-240px)] flex">
        {/* Conversation List */}
        <div className="w-80 border-r border-border flex flex-col">
          <div className="p-4 border-b border-border">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search conversations..."
                className="w-full pl-10 pr-4 py-2 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none text-sm"
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto">
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setSelectedChat(conv.id)}
                className={`w-full p-4 border-b border-border text-left hover:bg-muted/50 transition-colors ${
                  selectedChat === conv.id ? 'bg-muted' : ''
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-2xl flex-shrink-0">
                    {conv.logo}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="truncate text-sm">{conv.company}</h4>
                      <span className="text-xs text-muted-foreground">{conv.timestamp}</span>
                    </div>
                    <p className="text-xs text-muted-foreground mb-1">{conv.contact} • {conv.position}</p>
                    <p className="text-sm text-muted-foreground truncate">{conv.lastMessage}</p>
                  </div>
                  {conv.unread > 0 && (
                    <div className="w-5 h-5 rounded-full bg-primary flex items-center justify-center text-xs text-primary-foreground">
                      {conv.unread}
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Chat Window */}
        <div className="flex-1 flex flex-col">
          {selectedConversation ? (
            <>
              {/* Chat Header */}
              <div className="p-4 border-b border-border flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-xl">
                    {selectedConversation.logo}
                  </div>
                  <div>
                    <h4 className="text-sm">{selectedConversation.company}</h4>
                    <p className="text-xs text-muted-foreground">
                      {selectedConversation.contact} • {selectedConversation.position}
                    </p>
                  </div>
                </div>
                <button className="w-8 h-8 rounded-lg hover:bg-muted flex items-center justify-center transition-colors">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-md ${
                        message.sender === 'user'
                          ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white'
                          : 'bg-muted text-foreground'
                      } rounded-2xl px-4 py-3`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p
                        className={`text-xs mt-1 ${
                          message.sender === 'user' ? 'text-white/70' : 'text-muted-foreground'
                        }`}
                      >
                        {message.timestamp}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Message Input */}
              <div className="p-4 border-t border-border">
                <div className="flex items-center gap-2">
                  <button className="w-10 h-10 rounded-xl hover:bg-muted flex items-center justify-center transition-colors">
                    <Paperclip className="w-5 h-5" />
                  </button>
                  <input
                    type="text"
                    placeholder="Type your message..."
                    value={messageInput}
                    onChange={(e) => setMessageInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    className="flex-1 px-4 py-2.5 bg-input-background rounded-xl border border-transparent focus:border-primary focus:outline-none"
                  />
                  <button
                    onClick={handleSendMessage}
                    className="w-10 h-10 rounded-xl bg-primary text-primary-foreground hover:opacity-90 flex items-center justify-center transition-opacity"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-muted-foreground">
              <div className="text-center">
                <div className="w-16 h-16 rounded-2xl bg-muted mx-auto mb-4 flex items-center justify-center">
                  <Send className="w-8 h-8" />
                </div>
                <p>Select a conversation to start chatting</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
