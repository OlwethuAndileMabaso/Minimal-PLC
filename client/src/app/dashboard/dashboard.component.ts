import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {
  stats = [
    { label: 'Devices', value: '12', sub: '● Online', subClass: 'text-success' },
    { label: 'Active Tags', value: '48', sub: 'Polling active', subClass: '' },
    { label: 'Alarms', value: '3', sub: '🔴 Active', subClass: 'text-danger' },
    { label: 'Uptime', value: '99.9%', sub: 'Last 30 days', subClass: '' }
  ];

  recentAlarms = [
    { severity: 'critical', message: 'Zone 3 High Temp', time: '14:32' },
    { severity: 'warning', message: 'Supply Air Low', time: '13:15' },
    { severity: 'critical', message: 'Chiller Fault', time: '12:01' }
  ];

  connectedDevices = [
    { name: 'EasyIO FT-04', protocol: 'BACnet/IP', ip: '192.168.1.50', online: true },
    { name: 'EasyIO FW-14', protocol: 'BACnet/IP', ip: '192.168.1.51', online: true },
    { name: 'OpenPLC Runtime', protocol: 'Modbus TCP', ip: '192.168.1.10', online: false }
  ];

  refresh(): void {
    // Refresh data
  }
}
