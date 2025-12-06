import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TopGameService{
  baseUrl = "http://172.20.140.142:8080/"
  constructor(private http: HttpClient){}

  getTopSteamGames(): any{
    return this.http.get<any>(this.baseUrl + "get-top-games");
  }

  getSteamPage(gameName: string): any{
    return this.http.get<any>(this.baseUrl + "get-game-page/" + gameName);
  }

  getFeaturedSteamGames(): any{
    return this.http.get<any>(this.baseUrl + "get-featured-games");
  }

  getFeaturedCatGames(): any{
    return this.http.get<any>(this.baseUrl + "get-featured-categories");
  }

  postModelQuery(gameNames: string){
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post<any>(this.baseUrl + "query/" + gameNames, headers);
  }

  openSteamPage(gamePage: string){
    window.open(gamePage, '_blank');
  }
}
