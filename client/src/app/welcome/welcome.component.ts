import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.scss']
})
export class WelcomeComponent implements OnInit {
  greeting = 'Good morning';
  currentDate = new Date();

  recentProjects = [
    {
      icon: '🏢',
      name: 'Project One',
      lastOpened: 'today',
      devices: 12,
      alarms: 3
    },
    {
      icon: '🏭',
      name: 'Project Two',
      lastOpened: '2 days ago',
      devices: 8,
      alarms: 0
    }
  ];

  gettingStarted = [
    {
      step: 1,
      title: 'Add Device',
      description: 'Connect BACnet/IP, Modbus TCP, or OPC-UA devices',
      route: '/app/devices'
    },
    {
      step: 2,
      title: 'Map Tags',
      description: 'Map BACnet points and Modbus registers to tags',
      route: '/app/devices'
    },
    {
      step: 3,
      title: 'Design HMI',
      description: 'Drag & drop widgets onto your HMI canvas',
      route: '/app/hmi-designer'
    }
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {
    const hour = new Date().getHours();
    if (hour < 12) {
      this.greeting = 'Good morning';
    } else if (hour < 18) {
      this.greeting = 'Good afternoon';
    } else {
      this.greeting = 'Good evening';
    }
  }

  navigate(route: string): void {
    this.router.navigate([route]);
  }

  openProject(project: { name: string }): void {
    this.router.navigate(['/app/dashboard']);
  }
}
