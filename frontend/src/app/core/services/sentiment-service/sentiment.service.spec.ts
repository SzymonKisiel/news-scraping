import { TestBed } from '@angular/core/testing';

import { SentimentService } from './sentiment.service';

describe('CommandService', () => {
  let service: SentimentService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SentimentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
