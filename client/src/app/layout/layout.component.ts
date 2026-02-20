import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

interface NavItem {
  icon: string;
  label: string;
  route: string;
  badge?: number;
}

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {
  sidebarCollapsed = false;
  currentPageTitle = 'Dashboard';
  activeAlarms = 3;

  navItems: NavItem[] = [
    { icon: 'dashboard', label: 'Dashboard', route: '/app/dashboard' },
    { icon: 'palette', label: 'HMI Designer', route: '/app/hmi-designer' },
    { icon: 'settings_input_antenna', label: 'Devices', route: '/app/devices' },
    { icon: 'notifications_active', label: 'Alarms', route: '/app/alarms', badge: 3 },
    { icon: 'trending_up', label: 'Trends', route: '/app/trends' },
    { icon: 'description', label: 'Reports', route: '/app/trends' },
    { icon: 'group', label: 'Users', route: '/app/users' },
    { icon: 'settings', label: 'Settings', route: '/app/settings' }
  ];

  pageMap: Record<string, string> = {
    '/app/dashboard': 'Dashboard',
    '/app/hmi-designer': 'HMI Designer',
    '/app/devices': 'Devices',
    '/app/alarms': 'Alarms',
    '/app/trends': 'Trends',
    '/app/users': 'Users',
    '/app/settings': 'Settings'
  };

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.currentPageTitle = this.pageMap[event.urlAfterRedirects] || 'Dashboard';
    });
    this.currentPageTitle = this.pageMap[this.router.url] || 'Dashboard';
  }

  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  isActive(route: string): boolean {
    return this.router.url === route;
  }

  navigate(route: string): void {
    this.router.navigate([route]);
  }

  goHome(): void {
    this.router.navigate(['/']);
  }
}
