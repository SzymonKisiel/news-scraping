import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchTermsComponent } from './search-terms.component';

describe('SearchTermsComponent', () => {
  let component: SearchTermsComponent;
  let fixture: ComponentFixture<SearchTermsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchTermsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchTermsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
