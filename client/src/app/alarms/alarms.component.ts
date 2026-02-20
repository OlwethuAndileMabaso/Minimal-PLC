import { Component } from '@angular/core';

interface Alarm {
  severity: 'critical' | 'warning' | 'normal';
  message: string;
  time: string;
  acknowledged: boolean;
}

@Component({
  selector: 'app-alarms',
  templateUrl: './alarms.component.html',
  styleUrls: ['./alarms.component.scss']
})
export class AlarmsComponent {
  activeFilter = 'All';
  filters = ['All', 'Active', 'Today'];
  searchQuery = '';

  alarms: Alarm[] = [
    { severity: 'critical', message: 'Zone 3 Temp > 30°C', time: '14:32', acknowledged: false },
    { severity: 'warning', message: 'Supply Air < 15°C', time: '13:15', acknowledged: false },
    { severity: 'critical', message: 'Chiller Fault', time: '12:01', acknowledged: false },
    { severity: 'normal', message: 'Fan 1 restored', time: '11:45', acknowledged: true }
  ];

  get activeCount(): number {
    return this.alarms.filter(a => !a.acknowledged && a.severity !== 'normal').length;
  }

  get filteredAlarms(): Alarm[] {
    let result = this.alarms;
    if (this.activeFilter === 'Active') {
      result = result.filter(a => !a.acknowledged && a.severity !== 'normal');
    }
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(a => a.message.toLowerCase().includes(q));
    }
    return result;
  }

  setFilter(filter: string): void {
    this.activeFilter = filter;
  }

  acknowledge(alarm: Alarm): void {
    alarm.acknowledged = true;
  }

  acknowledgeAll(): void {
    this.alarms.forEach(a => a.acknowledged = true);
  }

  exportCSV(): void {
    // Export alarms as CSV
  }

  exportPDF(): void {
    // Export alarms as PDF
  }

  getSeverityIcon(severity: string): string {
    switch (severity) {
      case 'critical': return '🔴';
      case 'warning': return '🟡';
      case 'normal': return '✅';
      default: return '⚪';
    }
  }
}
