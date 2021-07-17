import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { 

  }

   getPoints(neLat: any, neLong: any, swLat:any, swLong: any) {
    let params = new HttpParams()
    .set('ne_lat', neLat)
    .set('ne_long', neLong)
    .set('sw_lat', swLat)
    .set('sw_long', swLong)

    return this.http.get('http://127.0.0.1:5000/api/data',  {
      params: params
    })
  }


}
