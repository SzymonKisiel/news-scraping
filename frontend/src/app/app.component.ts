import { Component, OnInit } from '@angular/core';
import { CommandService } from './core/services/command-service/command.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'news-scraping-ui';

  constructor() { }
}
