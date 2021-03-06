??          \      ?       ?   M  ?            '  <   H  '   ?     ?  P   ?  9    t  A     ?	  &   ?	  6   ?	  ,   .
  
   [
  U   f
                                       
            <p>Hello ${(object.partner_id.name)},<br><br>
            This email is being sent to notify you we have received a payment for this invoice with reference ${(object.invoice_ids[0].name)}.<br><br>
            Invoice number: ${(object.invoice_ids[0].name)}<br>
            Invoice due date: ${(object.invoice_ids[0].invoice_date_due)}<br>
            Invoice total amount: ${format_amount(object.invoice_ids[0].amount_total,object.currency_id)}<br><br>
            Paid amount: ${format_amount(object.amount,object.currency_id)}<br><br>
            After above payment(s) there is ${format_amount(object.invoice_ids[0].amount_residual,object.currency_id)} outstanding on invoice ${(object.invoice_ids[0].name)}.<br><br>
            Kind regards,<br>
            <strong>${(object.company_id.name)}</strong></p>
            
         Config Settings Notify invoice payment via email Payment received notice from ${(object.invoice_ids[0].name)} Payment_${(object.invoice_ids[0].name)} Payments Send payment received email to customer when a payment is registered on invoice. Project-Id-Version: Odoo Server 13.0-20200629
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-06-30 15:16+0200
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: Poedit 2.3
Last-Translator: 
Language: nl
 
            <p>Beste ${(object.partner_id.name)},<br><br>
            Deze e-mail is verzonden om te melden dat wij een betaling van u hebben ontvangen voor deze factuur met referentie ${(object.invoice_ids[0].name)}.<br><br>
            Factuurnummer: ${(object.invoice_ids[0].name)}<br>
            Factuur vervaldatum: ${(object.invoice_ids[0].invoice_date_due)}<br>
            Factuur totaalbedrag: ${format_amount(object.invoice_ids[0].amount_total,object.currency_id)}<br><br>
            Betaald bedrag: ${format_amount(object.amount,object.currency_id)}<br><br>
            Na bovengenoemde betaling(en) is er nog ${format_amount(object.invoice_ids[0].amount_residual,object.currency_id)} openstaand op factuur ${(object.invoice_ids[0].name)}.<br><br>
            Met vriendelijke groet,<br>
            <strong>${(object.company_id.name)}</strong></p>
            
         Configuratie-instellingen Notificatie factuurbetaling via e-mail Betaling ontvangen van ${(object.invoice_ids[0].name)} Betaalbewijs_${(object.invoice_ids[0].name)} Betalingen Stuur betaling ontvangen e-mail wanneer een betaling is geregistreerd op een factuur. 