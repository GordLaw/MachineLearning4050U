import { Component, OnInit } from '@angular/core';
import { CarouselModule } from 'primeng/carousel';
import { TopGameService } from '../../services/top-game.service';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-game-container',
  imports: [CarouselModule, ButtonModule],
  templateUrl: './game-container.component.html',
  styleUrl: './game-container.component.css'
})
export class GameContainerComponent implements OnInit {
  topGames: any[] = [];
  responsiveOptions: any[] | undefined;
  constructor(private topGameService: TopGameService){}
  ngOnInit(): void {
    this.topGameService.getTopSteamGames().subscribe((response: any) => {
      this.topGames = response.top_games;
    });

    this.responsiveOptions = [
      {
          breakpoint: '1400px',
          numVisible: 2,
          numScroll: 1
      },
      {
          breakpoint: '1199px',
          numVisible: 3,
          numScroll: 1
      },
      {
          breakpoint: '767px',
          numVisible: 2,
          numScroll: 1
      },
      {
          breakpoint: '575px',
          numVisible: 1,
          numScroll: 1
      }
    ]
  }

  openGamePage(gameName: any): void {
    this.topGameService.getSteamPage(gameName).subscribe((response: any) => {
      this.topGameService.openSteamPage(response.game_page);
    });
  }
}
