import { Component } from '@angular/core';

interface User {
  name: string;
  email: string;
  role: 'admin' | 'operator' | 'viewer';
  lastLogin: string;
}

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent {
  users: User[] = [
    { name: 'Admin User', email: 'admin@minimal-plc.io', role: 'admin', lastLogin: 'Just now' },
    { name: 'John Operator', email: 'john@example.com', role: 'operator', lastLogin: '2 hours ago' },
    { name: 'Sarah Viewer', email: 'sarah@example.com', role: 'viewer', lastLogin: 'Yesterday' }
  ];

  addUser(): void {
    // Open add user dialog
  }

  editUser(user: User): void {
    // Open edit user dialog
  }

  deleteUser(user: User): void {
    this.users = this.users.filter(u => u !== user);
  }

  getRoleBadgeClass(role: string): string {
    switch (role) {
      case 'admin': return 'badge-primary';
      case 'operator': return 'badge-success';
      case 'viewer': return 'badge-neutral';
      default: return 'badge-neutral';
    }
  }
}
