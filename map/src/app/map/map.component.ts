import { ApiService } from './../services/api.service';
import { Component, OnInit, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import 'leaflet.heat/dist/leaflet-heat.js'
import { addressPoints } from '../assets/realworld.1000';
import { NgxSpinnerService } from "ngx-spinner";

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, AfterViewInit {
  public options = {
    layers: [
      L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: ""
      })
    ],
    zoom: 12,
    center: L.latLng(37.87, -78.9814)
  };
  public searchType: boolean = false;
  private map: any;
  private heatLayer: any;

 
  constructor(
    private apiService: ApiService,
    private spinner: NgxSpinnerService
    ) { }

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


  public onMapReady(map: any) {
    this.map = map
    console.log('map', map)
    let newAddressPoints = addressPoints.map(function (p) { return [p[0], p[1]]; });
    const heat = (L as any).heatLayer(newAddressPoints).addTo(map);
  }

  public log(event: any) {
    this.spinner.show();
    this.initMap();
    console.log('event', event)
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

  private initMap(lng?:number, lon?:number): void {
    this.map =  L.map('map').setView([35.94, -78.9814], 12);
  }
}
