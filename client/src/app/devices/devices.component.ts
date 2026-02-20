import { Component } from '@angular/core';

interface Device {
  name: string;
  protocol: string;
  ip: string;
  tags: number;
  lastPoll: string;
  online: boolean;
}

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.scss']
})
export class DevicesComponent {
  activeFilter = 'All';
  filters = ['All', 'BACnet', 'Modbus', 'OPC-UA'];

  devices: Device[] = [
    {
      name: 'EasyIO FT-04',
      protocol: 'BACnet/IP',
      ip: '192.168.1.50',
      tags: 12,
      lastPoll: '2s ago',
      online: true
    },
    {
      name: 'EasyIO FW-14',
      protocol: 'BACnet/IP',
      ip: '192.168.1.51',
      tags: 8,
      lastPoll: '2s ago',
      online: true
    },
    {
      name: 'OpenPLC Runtime',
      protocol: 'Modbus TCP',
      ip: '192.168.1.10',
      tags: 24,
      lastPoll: '1s ago',
      online: true
    }
  ];

  get filteredDevices(): Device[] {
    if (this.activeFilter === 'All') return this.devices;
    return this.devices.filter(d =>
      d.protocol.toLowerCase().includes(this.activeFilter.toLowerCase())
    );
  }

  setFilter(filter: string): void {
    this.activeFilter = filter;
  }

  addDevice(): void {
    // Open add device dialog
  }

  editDevice(device: Device): void {
    // Open edit device dialog
  }
}
