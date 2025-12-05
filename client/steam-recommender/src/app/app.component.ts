import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from "./components/header/header.component";
import { InputComponent } from "./components/input/input.component";
import { CardModule } from 'primeng/card';
import { GameContainerComponent } from './components/game-container/game-container.component';
import { GameTableComponent } from './components/game-table/game-table.component';
import { GameHighlightComponent } from './components/game-highlight/game-highlight.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    HeaderComponent,
    CardModule,
    InputComponent,
    GameContainerComponent,
    GameTableComponent,
    GameHighlightComponent
],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Steam Recommender';
}
