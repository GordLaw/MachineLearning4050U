import { Component, OnInit, Input } from '@angular/core';
import { CarouselModule } from 'primeng/carousel';
import { TopGameService } from '../../services/top-game.service';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { ɵEmptyOutletComponent } from "@angular/router";

@Component({
  selector: 'app-game-container',
  imports: [CarouselModule, ButtonModule, CardModule],
  templateUrl: './game-carousel.component.html',
  styleUrl: './game-carousel.component.css'
})
export class GameCarouselComponent implements OnInit {
  @Input() inputData: any[] = [];
  responsiveOptions: any[] | undefined;

  constructor(private topGameService: TopGameService){}

  ngOnInit(): void {
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
