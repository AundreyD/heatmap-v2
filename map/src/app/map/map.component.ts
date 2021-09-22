import { ApiService } from './../services/api.service';
import { Component, OnInit } from '@angular/core';
import { addressPoints } from '../assets/realworld.1000';
import { NgxSpinnerService } from "ngx-spinner";
import * as L from 'leaflet';
import 'leaflet.heat/dist/leaflet-heat.js'

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  public coords = {
    latitude: 37.87,
    longitude: -78.9814
  }
  public options = {
    layers: [
      L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: ""
      })
    ],
    zoom: 12,
    center: L.latLng(this.coords.latitude, this.coords.longitude)
  };
  public searchType: boolean = false;
  private map: any;
  private heatLayer: any;

 
  constructor(
    private apiService: ApiService,
    private spinner: NgxSpinnerService
    ) { }

  ngOnInit(): void {
    window.navigator.geolocation.getCurrentPosition((position: GeolocationPosition) => {
      this.coords = position.coords
    })
  }

  public onMapReady(map: any) {
    this.map = map
    let newAddressPoints = addressPoints.map(function (p) { return [p[0], p[1]]; });
    const heat = (L as any).heatLayer(newAddressPoints).addTo(map);
  }

  public addHeatMapLayer(event: any) {
    this.spinner.show();
    if(this.heatLayer) { this.map.removeLayer(this.heatLayer)}
    let bounds = this.map.getBounds();
    let points: any;
    this.apiService.getPoints(bounds.getNorth().toFixed(2),bounds.getEast().toFixed(2), bounds.getSouth().toFixed(2), bounds.getWest().toFixed(2)).subscribe( data => {
      points = data;
      let newAddressPoints = points.map(function (p:any) { return [p['latitude'], p['longitude']]; });
      this.heatLayer = (L as any).heatLayer(newAddressPoints).addTo(this.map);
      this.spinner.hide()
    })
  }

  public ipToggle() {
    this.searchType = !this.searchType;
  }

  public getPosition(event: any, options?: PositionOptions): void {
    new Promise((resolve, reject) => 
        navigator.geolocation.getCurrentPosition(resolve, reject, options)
    )
    .then(() => {
      console.log('passed')
      console.log('event', event)
      this.onMapReady(event)
    })
    .catch(() =>{
      console.log('caught');
      this.onMapReady(event)
    });
  }
  
  private initMap(lng?:number, lon?:number): void {
    this.map =  L.map('map').setView([35.94, -78.9814], 12);
  }
}
