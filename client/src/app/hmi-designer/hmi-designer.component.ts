import { Component } from '@angular/core';
import { Router } from '@angular/router';

interface WidgetGroup {
  name: string;
  widgets: Widget[];
}

interface Widget {
  icon: string;
  label: string;
}

interface Layer {
  name: string;
  visible: boolean;
}

@Component({
  selector: 'app-hmi-designer',
  templateUrl: './hmi-designer.component.html',
  styleUrls: ['./hmi-designer.component.scss']
})
export class HmiDesignerComponent {
  searchQuery = '';
  selectedPanel: 'properties' | 'layers' = 'properties';

  widgetGroups: WidgetGroup[] = [
    {
      name: 'Shapes',
      widgets: [
        { icon: '▭', label: 'Rect' },
        { icon: '●', label: 'Circle' }
      ]
    },
    {
      name: 'Gauges',
      widgets: [
        { icon: '⊙', label: 'Gauge' },
        { icon: '▬', label: 'Bar' }
      ]
    },
    {
      name: 'Industrial',
      widgets: [
        { icon: '⬆', label: 'Pump' },
        { icon: '▼', label: 'Tank' },
        { icon: '⊠', label: 'Valve' }
      ]
    }
  ];

  layers: Layer[] = [
    { name: 'Layer 1', visible: true },
    { name: 'Layer 2', visible: true }
  ];

  constructor(private router: Router) {}

  save(): void {
    // Save HMI
  }

  preview(): void {
    // Preview HMI
  }

  goBack(): void {
    this.router.navigate(['/app/dashboard']);
  }

  addLayer(): void {
    this.layers.push({ name: `Layer ${this.layers.length + 1}`, visible: true });
  }

  toggleLayer(layer: Layer): void {
    layer.visible = !layer.visible;
  }

  importSVG(): void {
    // Import SVG file
  }
}
