# Author: Guillaume Beinse
# Reference: JCO CCI

# Generate_an_abstract_corpus from pubmed querry with RISmed R package version XX
# query used here: phase 1 clinical trials on cancers

install.packages("RISmed")
library(RISmed)

# query all requested studies on pubmed
research <- EUtilsSummary(query = c("clinical trial, phase i[Publication Type] 
AND neoplasms[MeSH Major Topic]) 
AND antineoplastic agents[MeSH Terms]) 
NOT antineoplastic combined chemotherapy protocols[MeSH Terms] 
AND (English[lang] AND adult[MeSH Terms])"),
                                type="esearch", db="pubmed", 
                                datetype='pdat', retmax=15000)


research_short_10 <- EUtilsSummary(query = c("clinical trial, phase i[Publication Type] 
AND neoplasms[MeSH Major Topic]) 
AND antineoplastic agents[MeSH Terms]) 
NOT antineoplastic combined chemotherapy protocols[MeSH Terms] 
AND (English[lang] AND adult[MeSH Terms])"),
                                  type="esearch", db="pubmed", 
                                  datetype='pdat', retmax=10)

# check how many studies have been found
QueryCount(research)
QueryId(research)

QueryCount(research_short_1)
QueryId(research_short_1)


# download results of the query from the pubmed database
RESULTS <- EUtilsGet(research,db = "pubmed")
RESULTS_short_10 <- EUtilsGet(research_short_10,db = "pubmed")

# get journal
journal <- MedlineTA(RESULTS_short_1)

# get title
Titles  <- ArticleTitle(RESULTS_short_1)

# get article ID
Art_ID <- ArticleId(RESULTS_short_1)

# get abstract
Abstracts <- AbstractText(RESULTS_short_1)

# get MeSH terms
MeSH <- Mesh(RESULTS_short_1)

# get PMID
PMID <- PMID(RESULTS_short_1)

# get abstract text and main features
pubmed_data_short_10 <- t(rbind(
  'PMID'=PMID(RESULTS_short_10),
  'Journal' = MedlineTA(RESULTS_short_10),
  'Year_publication'= YearPubmed(RESULTS_short_10),
  'Month_publication' = MonthPubmed(RESULTS_short_10),
  'Title'=ArticleTitle(RESULTS_short_10),
#  'Authors'= Author(RESULTS_short_10)[[1]],
#  'Volume'= Volume(RESULTS_short_10),
  'Abstract'=AbstractText(RESULTS_short_10)
#  'MeSH terms'=Mesh(RESULTS_short_10)
)
)

pubmed_data <- t(rbind(
  'PMID'=PMID(RESULTS),
  'Journal' = MedlineTA(RESULTS),
  'Year_publication'= YearPubmed(RESULTS),
  'Month_publication' = MonthPubmed(RESULTS),
  'Title'=ArticleTitle(RESULTS),
  #  'Authors'= Author(RESULTS_short_10)[[1]],
  #  'Volume'= Volume(RESULTS_short_10),
  'Abstract'=AbstractText(RESULTS)
  #  'MeSH terms'=Mesh(RESULTS_short_10)
)
)

View(head(pubmed_data))

# save results
write.table(pubmed_data, "pubmed_data_2606.txt", sep = "\t")
write.table(pubmed_data_short_10, "pubmed_data_short_10.txt", sep = "\t")            


            
