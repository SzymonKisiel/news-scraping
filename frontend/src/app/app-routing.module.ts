import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClientsComponent } from './components/clients/clients.component';
import { MaterialTestComponent } from './components/material-test/material-test.component';
import { ScraperComponent } from './components/scraper/scraper.component';
import { SearchTermsComponent } from './components/search-terms/search-terms.component';
import { SentimentsComponent } from './components/sentiments/sentiments.component';
import { TestComponent } from './components/test/test.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'clients', pathMatch: 'full'
  },
  // {
  //   path: 'test',
  //   component: TestComponent
  // },
  // {
  //   path: 'mat-test',
  //   component: MaterialTestComponent
  // },
  {
    path: 'scraper',
    component: ScraperComponent
  },
  {
    path: 'clients',
    component: ClientsComponent
  },
  {
    path: 'search-terms/:client-id',
    component: SearchTermsComponent
  },
  {
    path: 'sentiments/:search-term-id',
    component: SentimentsComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
