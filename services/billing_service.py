from models import Service, Agent, Discount, Job, Billing
from extensions import db
from datetime import datetime
import uuid

class BillingService:
    @staticmethod
    def calculate_job_price(job_id, additional_discount_percent=0.0, additional_charges=0.0):
        """
        Calculate the final price for a job including all discounts and charges
        """
        job = Job.query.get(job_id)
        if not job:
            return None
            
        # Get service base price
        service = Service.query.get(job.service_id)
        base_price = service.base_price if service else 0.0
        
        # Get base discount (system-wide discount)
        base_discount = Discount.query.filter_by(is_base_discount=True, is_active=True).first()
        base_discount_percent = base_discount.percent if base_discount else 0.0
        
        # Get agent discount
        agent = Agent.query.get(job.agent_id)
        agent_discount_percent = agent.agent_discount_percent if agent else 0.0
        
        # Calculate discount amounts
        base_discount_amount = (base_price * base_discount_percent) / 100
        agent_discount_amount = (base_price * agent_discount_percent) / 100
        additional_discount_amount = (base_price * additional_discount_percent) / 100
        
        # Calculate final price
        subtotal = base_price - base_discount_amount - agent_discount_amount - additional_discount_amount
        final_price = subtotal + additional_charges
        
        # Update job with calculated values
        job.base_price = base_price
        job.base_discount_percent = base_discount_percent
        job.agent_discount_percent = agent_discount_percent
        job.additional_discount_percent = additional_discount_percent
        job.additional_charges = additional_charges
        job.final_price = final_price
        
        db.session.commit()
        
        return {
            'base_price': base_price,
            'base_discount_percent': base_discount_percent,
            'base_discount_amount': base_discount_amount,
            'agent_discount_percent': agent_discount_percent,
            'agent_discount_amount': agent_discount_amount,
            'additional_discount_percent': additional_discount_percent,
            'additional_discount_amount': additional_discount_amount,
            'additional_charges': additional_charges,
            'subtotal': subtotal,
            'final_price': final_price
        }
    
    @staticmethod
    def create_invoice(job_id, due_date=None, notes=None, terms_conditions=None):
        """
        Create a billing invoice for a job
        """
        job = Job.query.get(job_id)
        if not job:
            return None
            
        # Generate invoice number
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Calculate pricing
        pricing = BillingService.calculate_job_price(job_id)
        if not pricing:
            return None
            
        # Create billing record
        billing = Billing(
            job_id=job_id,
            invoice_number=invoice_number,
            invoice_date=datetime.utcnow(),
            due_date=due_date or datetime.utcnow(),
            base_price=pricing['base_price'],
            base_discount_amount=pricing['base_discount_amount'],
            agent_discount_amount=pricing['agent_discount_amount'],
            additional_discount_amount=pricing['additional_discount_amount'],
            additional_charges=pricing['additional_charges'],
            subtotal=pricing['subtotal'],
            total_amount=pricing['final_price'],
            notes=notes,
            terms_conditions=terms_conditions
        )
        
        # Update job with invoice number
        job.invoice_number = invoice_number
        
        db.session.add(billing)
        db.session.commit()
        
        return billing
    
    @staticmethod
    def get_service_price(service_id):
        """
        Get the base price for a service
        """
        service = Service.query.get(service_id)
        return service.base_price if service else 0.0
    
    @staticmethod
    def get_agent_discount(agent_id):
        """
        Get the discount percentage for an agent
        """
        agent = Agent.query.get(agent_id)
        return agent.agent_discount_percent if agent else 0.0
    
    @staticmethod
    def get_base_discount():
        """
        Get the base discount percentage
        """
        base_discount = Discount.query.filter_by(is_base_discount=True, is_active=True).first()
        return base_discount.percent if base_discount else 0.0
    
    @staticmethod
    def generate_invoice_pdf(billing_id):
        """
        Generate PDF invoice (placeholder for PDF generation)
        """
        billing = Billing.query.get(billing_id)
        if not billing:
            return None
            
        # This would integrate with a PDF library like reportlab or weasyprint
        # For now, return the billing data for PDF generation
        return {
            'invoice_number': billing.invoice_number,
            'invoice_date': billing.invoice_date,
            'due_date': billing.due_date,
            'job': billing.job,
            'agent': billing.job.agent,
            'service': billing.job.service,
            'pricing_breakdown': {
                'base_price': billing.base_price,
                'base_discount': billing.base_discount_amount,
                'agent_discount': billing.agent_discount_amount,
                'additional_discount': billing.additional_discount_amount,
                'additional_charges': billing.additional_charges,
                'subtotal': billing.subtotal,
                'total': billing.total_amount
            },
            'notes': billing.notes,
            'terms_conditions': billing.terms_conditions
        } 