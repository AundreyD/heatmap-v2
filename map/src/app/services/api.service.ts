import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { 

  }

   getPoints(north: any, east: any, south:any, west: any, type: string = 'ipv4') {
    let params = new HttpParams()
    .set('north', north)
    .set('east', east)
    .set('south', south)
    .set('west', west)
    .set('type', type)

    return this.http.get('http://127.0.0.1:5000/api/data',  {
      params: params
    })
  }


}
