import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CoreModule } from './core/core.module';
import { TestComponent } from './components/test/test.component';
import { MaterialTestComponent } from './components/material-test/material-test.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { ClientsComponent } from './components/clients/clients.component';
import { SearchTermsComponent } from './components/search-terms/search-terms.component';
import { SentimentsComponent } from './components/sentiments/sentiments.component';
import { ScraperComponent } from './components/scraper/scraper.component';
import { ArticlesComponent } from './components/articles/articles.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    TestComponent,
    MaterialTestComponent,
    ClientsComponent,
    SearchTermsComponent,
    SentimentsComponent,
    ScraperComponent,
    ArticlesComponent
  ],
  imports: [
    CoreModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSlideToggleModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
