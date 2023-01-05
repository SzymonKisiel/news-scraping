export interface SearchTerm {
    id: number
    search_term: string
    updated_sentiments_at: Date
}

export interface SearchTerms {
    search_terms: SearchTerm[]
}