import { Component, OnInit } from '@angular/core';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-game-highlight',
  imports: [CardModule, ButtonModule],
  templateUrl: './game-highlight.component.html',
  styleUrl: './game-highlight.component.css'
})
export class GameHighlightComponent implements OnInit{
  featuredGame: any | undefined;

  ngOnInit(): void {
    
  }
}
