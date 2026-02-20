import { Component } from '@angular/core';

@Component({
  selector: 'app-trends',
  templateUrl: './trends.component.html',
  styleUrls: ['./trends.component.scss']
})
export class TrendsComponent {
  activeRange = '1H';
  timeRanges = ['1H', '6H', '24H', '7D', '30D', 'Custom'];

  selectedTags: string[] = ['Zone 3 Temp', 'Supply Air Temp'];
  availableTags = ['Zone 3 Temp', 'Supply Air Temp', 'Chiller Output', 'Fan Speed', 'Humidity'];

  setRange(range: string): void {
    this.activeRange = range;
  }

  removeTag(tag: string): void {
    this.selectedTags = this.selectedTags.filter(t => t !== tag);
  }

  exportCSV(): void {
    // Export chart data as CSV
  }

  exportPNG(): void {
    // Export chart as PNG
  }
}
