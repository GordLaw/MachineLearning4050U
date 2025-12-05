import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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

  getSteamPage(game_name: string): any{
    return this.http.get<any>(this.baseUrl + "get-game-page/" + game_name);
  }

  openSteamPage(gamePage: string){
    window.open(gamePage, '_blank');
  }
}
