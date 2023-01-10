import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
    private route: ActivatedRoute,
    private router: Router,
    private commandService: CommandService,
    private sentimentService: SentimentService) { }
  
  searchTerms: SearchTerm[] = [];
  // clientName: string = 'Szymon';
  clientId: number = 0;
  newSearchTerm: string = '';

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.clientId = params['client-id'];
      console.log(this.clientId)
      this.getAllSearchTerms();
    });

    // this.getAllSearchTerms();
  }

  getAllSearchTerms() {
    this.commandService.getAllSearchTermsByClientId(this.clientId).subscribe({
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

  navigateToSentiments(selectedSearchTerm: SearchTerm) {
    this.router.navigate(['/sentiments', selectedSearchTerm.id]);
  }

  onSubmit() {
    console.log(this.newSearchTerm)
    if (this.newSearchTerm == '') {
      return;
    }
    this.commandService.addSearchTermByClientId(this.clientId, this.newSearchTerm).subscribe({
      next: _ => {
      },
      error: err => {
        console.error('Observer got an error: ' + err);
        alert('Nieznany błąd serwera - nie udało się dodać nowej frazy.')
      },
      complete: () => {
        this.getAllSearchTerms();
        alert('Dodano nową frazę.')
      }
    });
  }
}
