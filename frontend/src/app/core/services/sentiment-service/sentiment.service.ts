import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Constants } from '../../model/constants';
import { API_URL } from '../../tokens';
import { Sentiments } from '../../model/sentiment';

@Injectable({
  providedIn: 'root'
})
export class SentimentService {

  constructor(
    @Inject(API_URL) private apiUrl: string,
    private httpClient: HttpClient) { }

  apiPath = '/api/command-handler/'

  getAllSentiments(search_term: string) {
    const action = 'get-all-sentiments'
    const url = this.apiUrl + this.apiPath + action
    
    return this.httpClient.get<Sentiments>(url, {
      params: {
        term: search_term
      }
    })
  }

  getAllSentimentsById(search_term_id: number) {
    const action = 'get-all-sentiments'
    const url = this.apiUrl + this.apiPath + action
    
    return this.httpClient.get<Sentiments>(url, {
      params: {
        term_id: search_term_id
      }
    })
  }
  
  updateSentiments(search_term: string) {
    const action = 'update-sentiments'
    const url = this.apiUrl + this.apiPath + action
    const body = {
      "search_term": search_term
    }

    return this.httpClient.post(url, body)
  }
}
