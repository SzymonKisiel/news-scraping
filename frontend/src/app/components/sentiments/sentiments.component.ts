import { Constants } from 'src/app/core/model/constants';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Sentiment } from 'src/app/core/model/sentiment';
import { SentimentService } from 'src/app/core/services/sentiment-service/sentiment.service';

@Component({
  selector: 'app-sentiments',
  templateUrl: './sentiments.component.html',
  styleUrls: ['./sentiments.component.css']
})
export class SentimentsComponent {
  constructor(
    private route: ActivatedRoute,
    private sentimentService: SentimentService) { }
  
  sentiments: Sentiment[] = [];
  // clientName: string = 'Szymon';
  // searchTerm: string = 'Banaś';
  searchTermId: number = 0;
  id2label = Constants.ID_2_LABEL;
  showScores = false;

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.searchTermId = params['search-term-id'];
      console.log(this.searchTermId)
      this.getAllSentiments();
    });
    // this.getAllSentiments();
  }

  getAllSentiments() {
    this.sentimentService.getAllSentimentsById(this.searchTermId).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        // console.log(clients);
        this.sentiments = x.sentiments;
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }
}
