import { Component, Input } from '@angular/core';
import { Card } from "primeng/card";
import { TopGameService } from '../../services/top-game.service';

@Component({
  selector: 'app-recommendation',
  imports: [Card],
  templateUrl: './recommendation.component.html',
  styleUrl: './recommendation.component.css'
})
export class RecommendationComponent {
  @Input() inputData: any[] = [];

  constructor(private topGameService: TopGameService){}

  openGamePage(gameName: any): void {
    this.topGameService.getSteamPage(gameName).subscribe((response: any) => {
      this.topGameService.openSteamPage(response.game_page);
    });
  }
}
