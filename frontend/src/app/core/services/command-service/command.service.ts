import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Constants } from '../../model/constants';
import { API_URL } from '../../tokens';
import { Clients } from '../../model/client';
import { SearchTerms } from '../../model/search_term';

@Injectable({
  providedIn: 'root'
})
export class CommandService {

  constructor(
    @Inject(API_URL) private apiUrl: string,
    private httpClient: HttpClient) { }

  apiPath = '/api/command-handler/'
  
  getAllClients() {
    const action = 'get-all-clients'
    const url = this.apiUrl + this.apiPath + action
    
    return this.httpClient.get<Clients>(url)
  }

  getAllSearchTerms(client_name: string) {
    const action = 'get-all-search-terms'
    const url = this.apiUrl + this.apiPath + action

    return this.httpClient.get<SearchTerms>(url, {
      params: {
        client_name: client_name
      }
    })
  }

  getAllSearchTermsByClientId(client_id: number) {
    const action = 'get-all-search-terms'
    const url = this.apiUrl + this.apiPath + action

    return this.httpClient.get<SearchTerms>(url, {
      params: {
        client_id: client_id
      }
    })
  }
  
  addClient(new_client_name: string) {
    const action = 'add-client'
    const url = this.apiUrl + this.apiPath + action
    const body = {
      "client_name": new_client_name
    }
    
    return this.httpClient.post(url, body)
  }

  addSearchTerm(client_name: string, new_search_term: string) {
    const action = 'add-search-term'
    const url = this.apiUrl + this.apiPath + action
    const body = {
      "client_name": client_name,
      "search_term": new_search_term
    }

    return this.httpClient.post(url, body)
  }
}
