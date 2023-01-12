import { keyframes } from '@angular/animations';
import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { interval, map, mergeMap, takeWhile, timer } from 'rxjs';
import { SearchTerm } from 'src/app/core/model/search_term';
import { CommandService } from 'src/app/core/services/command-service/command.service';
import { SentimentService } from 'src/app/core/services/sentiment-service/sentiment.service';
import { TaskStatuses } from 'src/app/core/model/task_status'

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

  searchTermsSpinners: { [key: string]: boolean } = {}

  checkForChanges = false;


  ngOnInit() {
    this.route.params.subscribe(params => {
      this.clientId = params['client-id'];
      console.log(this.clientId);
      this.getAllSearchTerms();
    });
    this.checkForSearchTermsChanges();
  }

  getAllSearchTerms() {
    this.commandService.getAllSearchTermsByClientId(this.clientId).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        // console.log(clients);
        this.searchTerms = x.search_terms;
        this.initSearchTermsSpinner();
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    });
  }

  initSearchTermsSpinner() {
    for (var searchTerm of this.searchTerms) {
      this.searchTermsSpinners[searchTerm.search_term] = false;
    }
  }

  checkForSearchTermsChanges() {
    this.checkForChanges = true;
    console.log('check for search term changes')
    timer(0, 5 * 1000)
      .pipe(
        takeWhile(_ => this.checkForChanges),
        mergeMap(() => this.sentimentService.getAllUpdateSentimentsTasks()),
      )
      .subscribe({
        next: x => {
          console.log('Test next');
          var tasks = x.tasks;
          console.log(tasks);

          var allTasksEnded = true;
          for (let searchTermName in tasks) {
            let taskStatus = tasks[searchTermName];
            let statusId = taskStatus.task_status_id;

            if (statusId == TaskStatuses.Started || statusId == TaskStatuses.Pending) {
              allTasksEnded = false;
              this.searchTermsSpinners[searchTermName] = true;
              console.log(`${searchTermName} = true`)
            }
            else {
              this.searchTermsSpinners[searchTermName] = false;
              console.log(`${searchTermName} = false`)
            }
          }
          console.log(allTasksEnded);
          if (allTasksEnded) {
            this.checkForChanges = false;
          }
        },
        error: err => console.error('Test error: ' + err),
        complete: () => console.log('Test complete')
      });
  }
  
  updateSentiments(searchTerm: SearchTerm) {
    this.searchTermsSpinners[searchTerm.id] = true;
    this.sentimentService.updateSentiments(searchTerm.search_term).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        console.log(x);
      },
      error: err => {
        console.error('Observer got an error: ' + err);
        this.searchTermsSpinners[searchTerm.id] = false;
      },
      complete: () => {
        console.log('Observer got a complete notification');
        this.checkForSearchTermsChanges();
      }
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
        alert('Pomyślnie dodano nową frazę.')
      }
    });
  }
}
