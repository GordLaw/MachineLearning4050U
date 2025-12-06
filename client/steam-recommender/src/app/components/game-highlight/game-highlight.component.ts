import { Component, Input } from '@angular/core';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-game-highlight',
  imports: [CardModule, ButtonModule],
  templateUrl: './game-highlight.component.html',
  styleUrl: './game-highlight.component.css'
})
export class GameHighlightComponent {
  @Input() inputData: any | undefined;
  featuredGame: any | undefined;

}
