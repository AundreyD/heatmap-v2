import { ApiService } from './../services/api.service';
import { Component, OnInit, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import 'leaflet.heat/dist/leaflet-heat.js'
import { addressPoints } from '../assets/realworld.1000'

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, AfterViewInit {
  options = {
    layers: [
      L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: ""
      })
    ],
    zoom: 12,
    center: L.latLng(37.87, -78.9814)
  };

  onMapReady(map: any) {
    this.map = map
    console.log('map', map)
    let newAddressPoints = addressPoints.map(function (p) { return [p[0], p[1]]; });
    const heat = (L as any).heatLayer(newAddressPoints).addTo(map);
  }

  private map: any;

  private initMap(): void {
    this.map =  L.map('map').setView([35.94, -78.9814], 12);
  }

 
  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    // this.initMap();
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      
    //   attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    // }).addTo(this.map);
    // let newAddressPoints = addressPoints.map(function (p) { return [p[0], p[1]]; });
    // addressPoints.map(function (p: any) { return [p[0], p[1]]; });

    // (L as any).heatLayer(addressPoints).addTo(this.map);

  }

  log(event: any) {
    console.log('event', event)
    console.log('pixel bounds', this.map.getPixelBounds());
    let bounds = this.map.getBounds();
    console.log('bounds', bounds)
    console.log('south', bounds.getSouth())
    console.log('west', bounds.getWest())
    console.log('East', bounds.getEast())
    console.log('North', bounds.getNorth())
    let ne = bounds._northEast;
    let sw = bounds._southWest;
    let points: any;
    this.apiService.getPoints(bounds.getEast().toFixed(2), bounds.getNorth().toFixed(2), bounds.getWest().toFixed(2), bounds.getSouth().toFixed(2)).subscribe( data => {
      points = data;
      let newAddressPoints = points.map(function (p:any) { return [p['latitude'], p['longitude']]; });
      const heat = (L as any).heatLayer(newAddressPoints).addTo(this.map);
    })
  }

}
