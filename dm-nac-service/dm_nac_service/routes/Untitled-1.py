SELFIE:

    doc=enrollmentDTO.customer.photoImageId


 

if filetype=PAN:

    condition: If "enrollmentDTO.customer.identityProof" is "Pan Card"

        enrollmentDTO.customer.identityProofImageId

   

AADHAR_DOC:

    condition: If "enrollmentDTO.customer.addressProof" is "Aadhar Card"

        enrollmentDTO.customer.addressProofImageId

 

loanDocuments:

    loanDTO.loanDocuments

 

    loanDTO.loanDocuments[].document

        loanDTO.loanDocuments[].documentId

 

    LOAN_APPLICATION:

    SANCTION_LETTER:

    LOAN_AGREEMENT:

    E_NASH (fileType: MITC):
