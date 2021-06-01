import { Component, OnInit, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, AfterViewInit {

  private map: any;

  private initMap(): void {
    this.map =  L.map('map').setView([51.505, -0.09], 13);
  }

 
  constructor() { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.initMap();
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 1,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);

    (L as any).heatLayer([
      // [50.5, 30.5, 0.2], //[51.505, -0.09]
      [51.505, -0.09, 0.4]
    ], {radius: 25}).addTo(this.map);
  }

}
