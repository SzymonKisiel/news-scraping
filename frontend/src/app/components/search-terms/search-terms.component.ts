import { Component } from '@angular/core';
import { SearchTerm } from 'src/app/core/model/search_term';
import { CommandService } from 'src/app/core/services/command-service/command.service';
import { SentimentService } from 'src/app/core/services/sentiment-service/sentiment.service';

@Component({
  selector: 'app-search-terms',
  templateUrl: './search-terms.component.html',
  styleUrls: ['./search-terms.component.css']
})
export class SearchTermsComponent {
  constructor(
    private commandService: CommandService,
    private sentimentService: SentimentService) { }
  
  searchTerms: SearchTerm[] = [];
  clientName: string = 'Szymon';

  ngOnInit() {
    this.getAllSearchTerms();
  }

  getAllSearchTerms() {
    this.commandService.getAllSearchTerms(this.clientName).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        // console.log(clients);
        this.searchTerms = x.search_terms;
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    });
  }
  
  updateSentiments(searchTerm: string) {
    this.sentimentService.updateSentiments(searchTerm).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        console.log(x);
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    });
  }
}
