import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Label } from '../ui/label';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { Switch } from '../ui/switch';
import { Separator } from '../ui/separator';
import { Bell, Lock, User, Globe } from 'lucide-react';

export function Settings() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2>Settings</h2>
        <p className="text-muted-foreground">Manage your account preferences and configurations</p>
      </div>

      {/* Company Profile */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-linear-to-br from-purple-400 to-purple-600 flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div>
              <CardTitle>Company Profile</CardTitle>
              <CardDescription>Update your company information</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Company Name</Label>
              <Input defaultValue="TechCorp Inc." className="bg-input-background border-border rounded-xl" />
            </div>
            <div className="space-y-2">
              <Label>Industry</Label>
              <Input defaultValue="Technology" className="bg-input-background border-border rounded-xl" />
            </div>
          </div>
          <div className="space-y-2">
            <Label>Company Website</Label>
            <Input defaultValue="https://techcorp.com" className="bg-input-background border-border rounded-xl" />
          </div>
          <Button className="bg-linear-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-xl">
            Save Changes
          </Button>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-linear-to-br from-blue-400 to-blue-600 flex items-center justify-center">
              <Bell className="w-5 h-5 text-white" />
            </div>
            <div>
              <CardTitle>Notifications</CardTitle>
              <CardDescription>Configure how you receive updates</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div>New Candidate Matches</div>
              <div className="text-sm text-muted-foreground">Get notified when new candidates match your jobs</div>
            </div>
            <Switch defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <div>Message Replies</div>
              <div className="text-sm text-muted-foreground">Receive alerts when candidates respond</div>
            </div>
            <Switch defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <div>Weekly Reports</div>
              <div className="text-sm text-muted-foreground">Get a summary of your recruitment activity</div>
            </div>
            <Switch />
          </div>
        </CardContent>
      </Card>

      {/* Mastodon Integration */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-linear-to-br from-purple-400 to-purple-600 flex items-center justify-center">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <div>
              <CardTitle>Mastodon Integration</CardTitle>
              <CardDescription>Connect your Mastodon instance</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Mastodon Instance URL</Label>
            <Input placeholder="https://mastodon.social" className="bg-input-background border-border rounded-xl" />
          </div>
          <div className="space-y-2">
            <Label>API Token</Label>
            <Input type="password" placeholder="Enter your API token" className="bg-input-background border-border rounded-xl" />
          </div>
          <Button variant="outline" className="rounded-xl border-border">
            Connect to Mastodon
          </Button>
        </CardContent>
      </Card>

      {/* Privacy & Security */}
      <Card className="rounded-2xl border-border shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-linear-to-br from-red-400 to-red-600 flex items-center justify-center">
              <Lock className="w-5 h-5 text-white" />
            </div>
            <div>
              <CardTitle>Privacy & Security</CardTitle>
              <CardDescription>Manage your account security</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button variant="outline" className="rounded-xl border-border">
            Change Password
          </Button>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <div>Two-Factor Authentication</div>
              <div className="text-sm text-muted-foreground">Add an extra layer of security</div>
            </div>
            <Switch />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
