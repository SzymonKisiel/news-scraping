import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClientsComponent } from './components/clients/clients.component';
import { MaterialTestComponent } from './components/material-test/material-test.component';
import { SearchTermsComponent } from './components/search-terms/search-terms.component';
import { SentimentsComponent } from './components/sentiments/sentiments.component';
import { TestComponent } from './components/test/test.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'test', pathMatch: 'full'
  },
  {
    path: 'test',
    component: TestComponent
  },
  {
    path: 'mat-test',
    component: MaterialTestComponent
  },
  {
    path: 'clients',
    component: ClientsComponent
  },
  // {
  //   path: 'search-terms',
  //   component: SearchTermsComponent
  // },
  {
    path: 'search-terms/:client_name',
    component: SearchTermsComponent
  },
  // {
  //   path: 'sentiments',
  //   component: SentimentsComponent
  // },
  {
    path: 'sentiments/:search_term',
    component: SentimentsComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
