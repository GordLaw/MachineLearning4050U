import { TestBed } from '@angular/core/testing';

import { TopGameService } from './top-game.service';

describe('TopGameService', () => {
  let service: TopGameService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TopGameService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
