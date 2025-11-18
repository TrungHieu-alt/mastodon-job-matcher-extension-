import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Separator } from '../ui/separator';
import { Send, DollarSign, Calendar, TrendingUp } from 'lucide-react';

const candidates = [
  { id: 1, name: 'Sarah Johnson', role: 'Senior Frontend Dev', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah', lastMessage: 'Thanks for the offer!', time: '2m ago', unread: 2 },
  { id: 2, name: 'Michael Chen', role: 'DevOps Engineer', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Michael', lastMessage: 'When can we discuss?', time: '1h ago', unread: 1 },
  { id: 3, name: 'Emily Rodriguez', role: 'Product Designer', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Emily', lastMessage: 'Sounds great!', time: '3h ago', unread: 0 },
  { id: 4, name: 'James Wilson', role: 'Backend Engineer', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=James', lastMessage: 'I appreciate the opportunity', time: '1d ago', unread: 0 },
];

const messages = [
  { id: 1, sender: 'them', text: 'Hi! Thanks for reaching out about the Senior Frontend Developer position.', time: '10:30 AM' },
  { id: 2, sender: 'me', text: 'Hi Sarah! We were really impressed with your portfolio. Would you be interested in discussing the role further?', time: '10:45 AM' },
  { id: 3, sender: 'them', text: 'Absolutely! I\'d love to learn more about the team and the projects.', time: '11:02 AM' },
  { id: 4, sender: 'me', text: 'Great! I\'ve prepared an offer for you. You can view the details in the offer summary above.', time: '11:15 AM' },
  { id: 5, sender: 'them', text: 'Thanks for the offer! This looks very competitive. I need a day to review everything.', time: '11:20 AM' },
];

export function OffersMessages() {
  const [selectedCandidate, setSelectedCandidate] = useState(candidates[0]);
  const [messageInput, setMessageInput] = useState('');

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
      {/* Candidate List */}
      <Card className="rounded-2xl border-border shadow-sm lg:col-span-1 overflow-hidden">
        <CardHeader>
          <CardTitle>Conversations</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-border">
            {candidates.map((candidate) => (
              <button
                key={candidate.id}
                onClick={() => setSelectedCandidate(candidate)}
                className={`w-full p-4 text-left hover:bg-accent transition-colors ${
                  selectedCandidate.id === candidate.id ? 'bg-accent' : ''
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className="relative">
                    <Avatar>
                      <AvatarImage src={candidate.avatar} />
                      <AvatarFallback>{candidate.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                    {candidate.unread > 0 && (
                      <div className="absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-br from-purple-500 to-purple-600 rounded-full flex items-center justify-center text-xs text-white">
                        {candidate.unread}
                      </div>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <div className="truncate">{candidate.name}</div>
                      <span className="text-xs text-muted-foreground">{candidate.time}</span>
                    </div>
                    <div className="text-sm text-muted-foreground truncate">{candidate.role}</div>
                    <div className="text-sm text-muted-foreground truncate mt-1">{candidate.lastMessage}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Chat & Offer Summary */}
      <div className="lg:col-span-2 space-y-4 flex flex-col">
        {/* Offer Summary Card */}
        <Card className="rounded-2xl border-border shadow-sm bg-gradient-to-br from-purple-50 to-white dark:from-purple-950/20 dark:to-card">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Offer Summary - {selectedCandidate.name}</CardTitle>
              <Badge className="bg-gradient-to-r from-purple-500 to-purple-600">
                Pending Review
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-green-100 dark:bg-green-950/50 flex items-center justify-center">
                  <DollarSign className="w-5 h-5 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Salary</div>
                  <div>$125,000</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-950/50 flex items-center justify-center">
                  <Calendar className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Start Date</div>
                  <div>Nov 15, 2024</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-950/50 flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Response</div>
                  <div>24h deadline</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Chat Interface */}
        <Card className="rounded-2xl border-border shadow-sm flex-1 flex flex-col">
          <CardHeader className="border-b border-border">
            <div className="flex items-center gap-3">
              <Avatar>
                <AvatarImage src={selectedCandidate.avatar} />
                <AvatarFallback>{selectedCandidate.name.charAt(0)}</AvatarFallback>
              </Avatar>
              <div>
                <CardTitle>{selectedCandidate.name}</CardTitle>
                <div className="text-sm text-muted-foreground">{selectedCandidate.role}</div>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'me' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                    message.sender === 'me'
                      ? 'bg-gradient-to-br from-purple-500 to-purple-600 text-white'
                      : 'bg-accent text-foreground'
                  }`}
                >
                  <p>{message.text}</p>
                  <div
                    className={`text-xs mt-1 ${
                      message.sender === 'me' ? 'text-purple-100' : 'text-muted-foreground'
                    }`}
                  >
                    {message.time}
                  </div>
                </div>
              </div>
            ))}
          </CardContent>

          <Separator />

          <div className="p-4">
            <div className="flex gap-2">
              <Input
                placeholder="Type a message..."
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                className="flex-1 bg-input-background border-border rounded-xl"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    setMessageInput('');
                  }
                }}
              />
              <Button 
                size="icon" 
                className="rounded-xl bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
