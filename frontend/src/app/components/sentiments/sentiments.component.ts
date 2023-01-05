import { Component } from '@angular/core';
import { Sentiment } from 'src/app/core/model/sentiment';
import { SentimentService } from 'src/app/core/services/sentiment-service/sentiment.service';

@Component({
  selector: 'app-sentiments',
  templateUrl: './sentiments.component.html',
  styleUrls: ['./sentiments.component.css']
})
export class SentimentsComponent {
  constructor(private sentimentService: SentimentService) { }
  
  sentiments: Sentiment[] = [];
  clientName: string = 'Szymon';
  searchTerm: string = 'Banaś';

  ngOnInit() {
    this.getAllSentiments();
  }

  getAllSentiments() {
    this.sentimentService.getAllSentiments(this.searchTerm).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        // console.log(clients);
        this.sentiments = x.sentiments;
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }
  // getAllClients() {
  //   this.commandService.getAllSearchTerms(this.clientName).subscribe({
  //     next: x => {
  //       console.log('Observer got a next value: ');
  //       // console.log(clients);
  //       this.searchTerms = x.search_terms;
  //     },
  //     error: err => console.error('Observer got an error: ' + err),
  //     complete: () => console.log('Observer got a complete notification')
  //   });
  // }
  
}
