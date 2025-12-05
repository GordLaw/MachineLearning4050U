import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameHighlightComponent } from './game-highlight.component';

describe('GameHighlightComponent', () => {
  let component: GameHighlightComponent;
  let fixture: ComponentFixture<GameHighlightComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GameHighlightComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GameHighlightComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
