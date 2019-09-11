<!DOCTYPE html>
<!-- Author: Nesrine Yahmed 2019-->

<html>
	<head>
		<meta charset="utf-8">
		<title>RESOLVED2</title>
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link href="css/bootstrap.css" rel="stylesheet">
		<script type="text/javascript" src="js/resolved2.js"></script>
	</head>

	<body id="bodyy" style="background-image: url('img/bg.jpg'); ">
		<div class="container">
			<div class="card-header">
				<h3>RESOLVED2</h3>
				<h6>
					The development of a cancer drug is currently long, costly and requires the involvement of 
					several thousand patients. Yet only 5% of these drugs will be effective enough to be 
					approved for cancer treatment.</br>
					RESOLVED2 is a machine-learning method that predicts the approval of a drug at the end of 
					a Phase I clinical trial. Phase I clinical studies are very early in the development of 
					a drug, and RESOLVED2 requires an average of only 30 patients to make predictions. When 
					RESOLVED2 predicts that a treatment will be approved, 73% of the treatments are actually 
					approved within 6 years, and the rest in subsequent years.</br>
					RESOLVED2 is also correct for 92% of treatments that will not be approved in 6 years. 
					RESOLVED2 has the potential to reduce the number of patients to be included in clinical 
					trials, by increasing the likelihood of routine use of treatment from 5% to 73%. 
					A prospective evaluation is planned to confirm the usefulness of routine use of RESOLVED2.
				</h6>
				<img src="img/fig.png" style="width:100%; "/>
			</div>
			
			<div class="card-body">
				
				<form action="" method="POST">	
					<table class="table table-striped">
						<thead>
							<tr>
								<th>
									<h4>RESOLVED2 is easy to use. Fill this form to get the approval predictions of your drug.</h4>
								</th>
							</tr>
						</thead>
					</table>
					<table class="table table-striped">
						<tbody>
							<tr>						
							<td>The treatment's name</td>
							<td>
								<input type="text" required="required" name="name" class="form-control" id="name" aria-describedby="TreatmentName" style="width:100%;">
							</td>							
							</tr>
						</tbody>
					</table>
					<table class="table table-striped">
						<tbody>
							<tr>						
							<td id="v1">Did this study include patients with an enrichment in a specific tumor type?</td>
							<td>
								<input class="form-check-input" type="radio" name="v1Res" id="v1YesId" value="Yes" >
								<label class="form-check-label" for="v1YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v1Res" id="v1NoId" value="No" >
								<label class="form-check-label" for="v1NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v1Res" id="v1NaId" value="NA">
								<label class="form-check-label" for="v1NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v2">Did this study planned a dose expansion cohort?</td>
							<td>
								<input class="form-check-input" type="radio" name="v2Res" id="v2YesId" value="Yes" >
								<label class="form-check-label" for="v2YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v2Res" id="v2NoId" value="No" >
								<label class="form-check-label" for="v2NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v2Res" id="v2NaId" value="NA">
								<label class="form-check-label" for="v2NaId" ><h6>NA</h6></label>
							</td>
							</tr>
							<tr>						
							<td  id="v3">Did this study consider molecular biomarkers for patients selection?</td>
							<td>
								<input class="form-check-input" type="radio" name="v3Res" id="v3YesId" value="Yes" >
								<label class="form-check-label" for="v3YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v3Res" id="v3NoId" value="No" >
								<label class="form-check-label" for="v3NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v3Res" id="v3NaId" value="NA">
								<label class="form-check-label" for="v3NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v4">Were there complete responses observed?</td>
							<td>
								<input class="form-check-input" type="radio" name="v4Res" id="v4YesId" value="Yes" >
								<label class="form-check-label" for="v4YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v4Res" id="v4NoId" value="No" >
								<label class="form-check-label" for="v4NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v4Res" id="v4NaId" value="NA">
								<label class="form-check-label" for="v4NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v5">Is the drug an antibody?</td>
							<td>
								<input class="form-check-input" type="radio" name="v5Res" id="v5YesId" value="Yes" >
								<label class="form-check-label" for="v5YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v5Res" id="v5NoId" value="No" >
								<label class="form-check-label" for="v5NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v5Res" id="v5NaId" value="NA">
								<label class="form-check-label" for="v5NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v6">Is the drug a BCRP-ABCG2 inhibitors?</td>
							<td>
								<input class="form-check-input" type="radio" name="v6Res" id="v6YesId" value="Yes" >
								<label class="form-check-label" for="v6YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v6Res" id="v6NoId" value="No" >
								<label class="form-check-label" for="v6NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v6Res" id="v6NaId" value="NA">
								<label class="form-check-label" for="v6NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v7">Is the drug a cytochrome P 450/CYP2C8 substrate?</td>
							<td>
								<input class="form-check-input" type="radio" name="v7Res" id="v7YesId" value="Yes" >
								<label class="form-check-label" for="v7YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v7Res" id="v7NoId" value="No" >
								<label class="form-check-label" for="v7NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v7Res" id="v7NaId" value="NA">
								<label class="form-check-label" for="v7NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v8">Is the drug a cytochrome P 450/CYP2C9 substrate?</td>
							<td>
								<input class="form-check-input" type="radio" name="v8Res" id="v8YesId" value="Yes" >
								<label class="form-check-label" for="v8YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v8Res" id="v8NoId" value="No" >
								<label class="form-check-label" for="v8NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v8Res" id="v8NaId" value="NA">
								<label class="form-check-label" for="v8NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v9">Is the drug a weak cytochrome P 450/CYP2D6 inhibitor?</td>
							<td>
								<input class="form-check-input" type="radio" name="v9Res" id="v9YesId" value="Yes" >
								<label class="form-check-label" for="v9YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v9Res" id="v9NoId" value="No" >
								<label class="form-check-label" for="v9NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v9Res" id="v9NaId" value="NA">
								<label class="form-check-label" for="v9NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v10">Is the drug a cytochrome P 450/CYP3A inducer?</td>
							<td>
								<input class="form-check-input" type="radio" name="v10Res" id="v10YesId" value="Yes" >
								<label class="form-check-label" for="v10YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v10Res" id="v10NoId" value="No" >
								<label class="form-check-label" for="v10NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v10Res" id="v10NaId" value="NA">
								<label class="form-check-label" for="v10NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v11">Is the drug a cytochrome P 450/CYP3A4 substrate?</td>
							<td>
								<input class="form-check-input" type="radio" name="v11Res" id="v11YesId" value="Yes" >
								<label class="form-check-label" for="v11YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v11Res" id="v11NoId" value="No" >
								<label class="form-check-label" for="v11NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v11Res" id="v11NaId" value="NA">
								<label class="form-check-label" for="v11NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v12">Is the drug a cytochrome P450 inhibitor?</td>
							<td>
								<input class="form-check-input" type="radio" name="v12Res" id="v12YesId" value="Yes" >
								<label class="form-check-label" for="v12YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v12Res" id="v12NoId" value="No" >
								<label class="form-check-label" for="v12NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v12Res" id="v12NaId" value="NA">
								<label class="form-check-label" for="v12NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v13">Is the drug a hypotensive agent?</td>
							<td>
								<input class="form-check-input" type="radio" name="v13Res" id="v13YesId" value="Yes" >
								<label class="form-check-label" for="v13YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v13Res" id="v13NoId" value="No" >
								<label class="form-check-label" for="v13NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v13Res" id="v13NaId" value="NA">
								<label class="form-check-label" for="v13NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v14">Is the drug a kinase inhibitor?</td>
							<td>
								<input class="form-check-input" type="radio" name="v14Res" id="v14YesId" value="Yes" >
								<label class="form-check-label" for="v14YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v14Res" id="v14NoId" value="No" >
								<label class="form-check-label" for="v14NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v14Res" id="v14NaId" value="NA">
								<label class="form-check-label" for="v14NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v15">Is the drug used as a miscellaneous skin and mucous membrane agents?</td>
							<td>
								<input class="form-check-input" type="radio" name="v15Res" id="v15YesId" value="Yes" >
								<label class="form-check-label" for="v15YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v15Res" id="v15NoId" value="No" >
								<label class="form-check-label" for="v15NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v15Res" id="v15NaId" value="NA">
								<label class="form-check-label" for="v15NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v16">Is the drug a nucleic acid synthesis inhibitor?</td>
							<td>
								<input class="form-check-input" type="radio" name="v16Res" id="v16YesId" value="Yes" >
								<label class="form-check-label" for="v16YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v16Res" id="v16NoId" value="No" >
								<label class="form-check-label" for="v16NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v16Res" id="v16NaId" value="NA">
								<label class="form-check-label" for="v16NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v17">Is the drug a P-glycoprotein/ABCB1 inhibitor?</td>
							<td>
								<input class="form-check-input" type="radio" name="v17Res" id="v17YesId" value="Yes" >
								<label class="form-check-label" for="v17YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v17Res" id="v17NoId" value="No" >
								<label class="form-check-label" for="v17NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v17Res" id="v17NaId" value="NA">
								<label class="form-check-label" for="v17NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v18">Is the drug a P-glycoprotein/ABCB1 substrate?</td>
							<td>
								<input class="form-check-input" type="radio" name="v18Res" id="v18YesId" value="Yes" >
								<label class="form-check-label" for="v18YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v18Res" id="v18NoId" value="No" >
								<label class="form-check-label" for="v18NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v18Res" id="v18NaId" value="NA">
								<label class="form-check-label" for="v18NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v19">Is the drug a protein?</td>
							<td>
								<input class="form-check-input" type="radio" name="v19Res" id="v19YesId" value="Yes" >
								<label class="form-check-label" for="v19YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v19Res" id="v19NoId" value="No" >
								<label class="form-check-label" for="v19NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v19Res" id="v19NaId" value="NA">
								<label class="form-check-label" for="v19NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v20">Is the drug a purine analogue?</td>
							<td>
								<input class="form-check-input" type="radio" name="v20Res" id="v20YesId" value="Yes" >
								<label class="form-check-label" for="v20YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v20Res" id="v20NoId" value="No" >
								<label class="form-check-label" for="v20NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v20Res" id="v20NaId" value="NA">
								<label class="form-check-label" for="v20NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v21">Is the drug a transferase?</td>
							<td>
								<input class="form-check-input" type="radio" name="v21Res" id="v21YesId" value="Yes" >
								<label class="form-check-label" for="v21YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v21Res" id="v21NoId" value="No" >
								<label class="form-check-label" for="v21NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v21Res" id="v21NaId" value="NA">
								<label class="form-check-label" for="v21NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td  id="v22">Does the drug target the C1q sub-complement subunit A?</td>
							<td>
								<input class="form-check-input" type="radio" name="v22Res" id="v22YesId" value="Yes" >
								<label class="form-check-label" for="v22YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v22Res" id="v22NoId" value="No" >
								<label class="form-check-label" for="v22NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v22Res" id="v22NaId" value="NA">
								<label class="form-check-label" for="v22NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v23">Does the drug target DNA?</td>
							<td>
								<input class="form-check-input" type="radio" name="v23Res" id="v23YesId" value="Yes" >
								<label class="form-check-label" for="v23YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v23Res" id="v23NoId" value="No" >
								<label class="form-check-label" for="v23NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v23Res" id="v23NaId" value="NA">
								<label class="form-check-label" for="v23NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v24">Does the drug target DNA polymerase alpha catalytic subunit?</td>
							<td>
								<input class="form-check-input" type="radio" name="v24Res" id="v24YesId" value="Yes" >
								<label class="form-check-label" for="v24YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v24Res" id="v24NoId" value="No" >
								<label class="form-check-label" for="v24NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v24Res" id="v24NaId" value="NA">
								<label class="form-check-label" for="v24NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v25">Does the drug target histone deacetylase 1?</td>
							<td>
								<input class="form-check-input" type="radio" name="v25Res" id="v25YesId" value="Yes" >
								<label class="form-check-label" for="v25YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v25Res" id="v25NoId" value="No" >
								<label class="form-check-label" for="v25NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v25Res" id="v25NaId" value="NA">
								<label class="form-check-label" for="v25NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v26">Does the drug target the low affinity immunoglobulin gamma Fc region receptor II-b?</td>
							<td>
								<input class="form-check-input" type="radio" name="v26Res" id="v26YesId" value="Yes" >
								<label class="form-check-label" for="v26YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v26Res" id="v26NoId" value="No" >
								<label class="form-check-label" for="v26NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v26Res" id="v26NaId" value="NA">
								<label class="form-check-label" for="v26NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v27">Does the drug target PDGFR-alpha 1?</td>
							<td>
								<input class="form-check-input" type="radio" name="v27Res" id="v27YesId" value="Yes" >
								<label class="form-check-label" for="v27YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v27Res" id="v27NoId" value="No" >
								<label class="form-check-label" for="v27NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v27Res" id="v27NaId" value="NA">
								<label class="form-check-label" for="v27NaId" ><h6>NA</h6></label>
							</td>
							</tr>

							<tr>						
							<td id="v28">Does the drug target PD-L1?</td>
							<td>
								<input class="form-check-input" type="radio" name="v28Res" id="v28YesId" value="Yes" >
								<label class="form-check-label" for="v28YesId"><h6>Yes</h6></label>					
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v28Res" id="v28NoId" value="No" >
								<label class="form-check-label" for="v28NoId"><h6>No</h6></label>	
										
							</td>
							<td>
								<input class="form-check-input" type="radio" name="v28Res" id="v28NaId" value="NA">
								<label class="form-check-label" for="v28NaId" ><h6>NA</h6></label>
							</td>
							</tr>
						</tbody>
					</table>
					
					<table class="table table-striped">
						<tbody>
							<tr>
							<td id="check" scope="col"><b>Has the drug already been approved?</b></td>
							<td scope="col">
								<input class="form-check-input" type="radio" name="checkRes" id="yesId" value="Yes" 
									onchange="getElementById('userResults').setAttribute('placeholder','How long did it take to be approved?');
											  getElementById('userResults').disabled=false;">
								<label class="form-check-label" for="yesId">
								<h6>Yes</h6>
								</label>
							</td>
							<td scope="col">
								<input class="form-check-input" type="radio" name="checkRes" id="noId" value="No" 
								onchange="getElementById('userResults').setAttribute('placeholder','When did the clinical trials start?');
										  getElementById('userResults').disabled=false;">
								<label class="form-check-label" for="noId">
								<h6>No</h6>
								</label>
							</td>
							<td scope="col">
							<input type="text" pattern="[0-9]{1,3}" required="required" name="oldResults" class="form-control" id="userResults" aria-describedby="userResults" disabled>
							<small id="rule">Enter the number of months [1-120]</small>
							</td>
							
							</tr>
						</tbody>
					</table>				
									
					<input name="submit" id="submitButton" type="submit" value="Submit" class="btn btn-outline-primary btn-rounded waves-effect btn-sm" />                                   
				</form>
				
				<?php
				
							//Connexion avec la BDD
							$user = 'root';
							$password = '';
							$server = 'localhost';
							$database = 'resolved2';
							$pdo = new PDO("mysql:host=$server;dbname=$database", $user, $password);  
							if (isset($_POST['submit'])){
							//Controle de saisie
							$test=true;
							for ($i=0;$i<28;$i++)
							{
								$n='v'.($i+1).'Res'; 	
								if (!(isset($_POST[$n]))) {
									$test=false;
									echo '<script type="text/javascript">
										var x=document.getElementById("v'.($i+1).'");
										x.style.color="red";
										</script>';
								}
								else {
									$yes='v'.($i+1).'YesId';
									$no='v'.($i+1).'NoId';
									$na='v'.($i+1).'NaId';
									if ($_POST[$n] == 'Yes') 
										echo '<script type="text/javascript">
										var x=document.getElementById("'.$yes.'");
										x.setAttribute("checked","checked");
										</script>';

									elseif  ($_POST[$n] == 'No') 
										echo '<script type="text/javascript">
										var x=document.getElementById("'.$no.'");
										x.setAttribute("checked","checked");
										</script>';
									else
										echo '<script type="text/javascript">
										var x=document.getElementById("'.$na.'");
										x.setAttribute("checked","checked");
										</script>';
								}
							}
							if (!isset($_POST['checkRes'])) {
								$test=false;
								echo '<script type="text/javascript">
										var x=document.getElementById("check");
										x.style.color="red";
										</script>';
							}
							if (isset($_POST['checkRes']) && !isset($_POST['oldResults'])) {
								$test=false;								
							}
							

							if ($test==true){ 
								echo "<h4>Results:</br></h4>";
								echo '<style type="text/css">
									.table {
										display:none;
									}
									.btn{
										display:none;
									}</style>'; 
								
								//Old results
								$r=0;
								if (isset($_POST['oldResults'])) $r=$_POST['oldResults']; 
								if ($_POST['checkRes'] == 'Yes') $b=1; if ($_POST['checkRes'] == 'No') $b=0;
								
								$d=$_POST['name'];
								//Récuperation des données
								$t = array();
								for ($j=0;$j<28;$j++){
									$x='v'.($j+1).'Res';         
									if ($_POST[$x] == 'Yes') $t[$j]=1; elseif  ($_POST[$x] == 'No') $t[$j]=0; else $t[$j]=0.5;            
								}

								//Coefficients
								$c = array(0.249363057057461, 0.217034723636037, 0.0485575995624746,0.309855654092673, 0.142909634065455,
											0.0775006866348778, 0.854868713008868, 0.795080208656765, 0.108343381991098, 0.103535144969705, 
											0.640177260853813, 0.538382574852804, 1.46228217730834, 1.55886852570061, 0.572119192668305,
											0.149839697267163, 0.157937719652731, 0.845023738244965, 0.129987904644142, 0.830975963836635, 
											1.832456023364, 1.96398388774414, 0.245078947971432, 0.00468413390687886, 0.395424888778408, 
											0.0309730010202191, 1.44203612625991, 1.59890614086357);

								//Calcul du résultat
								$result=0;
								for ($i=0; $i<28; $i++){
									$result+=$t[$i]*$c[$i];
								}
								
								if ($result>4.553632)								
									echo "<h5>The drug belongs to the second group. 92% of the drugs that are in this group are still not approved at 6 years.</h5>";
								else echo "<h5>The drug belongs to the first group. 73% of the drugs that are in this group are approved at 6 years.</h5>";
							
								//insertion dans la BDD
								$valeurs = ['drugName'=>$d, 'v1'=>$t[0], 'v2'=>$t[1], 'v3'=>$t[2], 'v4'=>$t[3], 'v5'=>$t[4], 'v6'=>$t[5], 'v7'=>$t[6],
											'v8'=>$t[7], 'v9'=>$t[8], 'v10'=>$t[9], 'v11'=>$t[10], 'v12'=>$t[11], 'v13'=>$t[12],
											'v14'=>$t[13], 'v15'=>$t[14], 'v16'=>$t[15], 'v17'=>$t[16], 'v18'=>$t[17], 'v19'=>$t[18],
											'v20'=>$t[19], 'v21'=>$t[20], 'v22'=>$t[21], 'v23'=>$t[22], 'v24'=>$t[23], 'v25'=>$t[24],
											'v26'=>$t[25], 'v27'=>$t[26], 'v28'=>$t[27], 'hasResults'=>$b, 'oldResults'=> $r];

								$sql = 'INSERT INTO user (drugName, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, hasResults, oldResults) 
												VALUES (:drugName, :v1, :v2, :v3, :v4, :v5, :v6, :v7, :v8, :v9, :v10, :v11, :v12, :v13, :v14, :v15, :v16, :v17, :v18, :v19, :v20, :v21, :v22, :v23, :v24, :v25, :v26, :v27, :v28, :hasResults, :oldResults)';

								
								$sql_preparee = $pdo->prepare($sql);
								if (!$sql_preparee){
									echo "\nPDO::errorInfo():\n";
									print_r($pdo->errorInfo());
								}
								$sql_preparee->execute($valeurs);
								$pdo=null;
							
							}				
							}?>
			</div>
		</div>
	</body>
</html>
