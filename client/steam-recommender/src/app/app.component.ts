import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { HeaderComponent } from "./components/header/header.component";
import { InputComponent } from "./components/input/input.component";
import { CardModule } from 'primeng/card';
import { GameCarouselComponent } from './components/game-carousel/game-carousel.component';
import { GameTableComponent } from './components/game-table/game-table.component';
import { GameHighlightComponent } from './components/game-highlight/game-highlight.component';
import { TopGameService } from './services/top-game.service';
import { RecommendationComponent } from './components/recommendation/recommendation.component';
import { DividerModule } from 'primeng/divider';
import { ViewportScroller } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [
    HeaderComponent,
    CardModule,
    InputComponent,
    GameCarouselComponent,
    GameTableComponent,
    GameHighlightComponent,
    RecommendationComponent,
    DividerModule,
],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  @ViewChild('targetSection') targetSection!: ElementRef;
  title = 'Steam Recommender';

  featuredGames: any | undefined;
  featuredCatGames: any | undefined;
  featuredCatGameA: any | undefined;
  featuredCatGameB: any | undefined;
  featuredCatGameC: any | undefined;
  featuredCatGameD: any | undefined;
  featuredSpecialGames: any | undefined;
  featuredTopGames: any | undefined;
  featuredNewGames: any | undefined;
  recommendedgames: any[] = [];

  constructor(private router: Router, private topGameService: TopGameService, private viewportScroller: ViewportScroller){}
  
  ngOnInit(): void {
    this.topGameService.getFeaturedSteamGames().subscribe((response: any) => {
      this.featuredGames = response.top_games;
    });
    this.topGameService.getFeaturedCatGames().subscribe((response: any) => {
      this.featuredCatGames = response.top_cat_games;
      this.featuredCatGameA = this.featuredCatGames[0].items[0];
      this.featuredCatGameB = this.featuredCatGames[1].items[0];
      this.featuredCatGameC = this.featuredCatGames[2].items[0];
      this.featuredCatGameD = this.featuredCatGames[3].items[0];
      this.featuredSpecialGames = response.top_cat_games.specials
      this.featuredTopGames = response.top_cat_games.top_sellers
      this.featuredNewGames = response.top_cat_games.new_releases
      console.log(this.featuredTopGames)
    });
  }

  handleChildEvent(sectionId: string){
    this.router.navigate([], {fragment: sectionId})
  }

  receiveMessage(message: string) {
    console.log(message);
    this.topGameService.postModelQuery(message).subscribe((response: any) => {
      this.recommendedgames = response.recommended_games;
      console.log(response)
    });
  }
}
