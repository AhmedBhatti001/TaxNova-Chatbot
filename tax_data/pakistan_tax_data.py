"""
Pakistan Tax Data Module
Contains structured data about Pakistan's tax system for quick reference
"""

from datetime import datetime
from typing import Dict, List, Any

class PakistanTaxData:
    """Pakistan tax system data and calculations"""
    
    def __init__(self):
        self.current_tax_year = "2024-25"
        self.tax_slabs = self._get_current_tax_slabs()
        self.important_dates = self._get_important_dates()
        self.deductions = self._get_deductions_data()
        self.withholding_rates = self._get_withholding_rates()
    
    def _get_current_tax_slabs(self) -> List[Dict[str, Any]]:
        """Get current individual income tax slabs"""
        return [
            {
                "min_income": 0,
                "max_income": 600000,
                "rate": 0,
                "description": "No tax"
            },
            {
                "min_income": 600001,
                "max_income": 1200000,
                "rate": 2.5,
                "description": "2.5% on income above Rs. 600,000"
            },
            {
                "min_income": 1200001,
                "max_income": 2200000,
                "rate": 12.5,
                "description": "12.5% on income above Rs. 1,200,000"
            },
            {
                "min_income": 2200001,
                "max_income": 3200000,
                "rate": 20,
                "description": "20% on income above Rs. 2,200,000"
            },
            {
                "min_income": 3200001,
                "max_income": 4100000,
                "rate": 25,
                "description": "25% on income above Rs. 3,200,000"
            },
            {
                "min_income": 4100001,
                "max_income": float('inf'),
                "rate": 35,
                "description": "35% on income above Rs. 4,100,000"
            }
        ]
    
    def _get_important_dates(self) -> Dict[str, str]:
        """Get important tax filing dates"""
        return {
            "salaried_individuals": "September 30",
            "non_salaried_individuals": "December 31",
            "companies": "December 31",
            "aop": "December 31",
            "wealth_statement": "December 31",
            "advance_tax_quarterly": "15th of month following quarter end"
        }
    
    def _get_deductions_data(self) -> Dict[str, Dict[str, Any]]:
        """Get tax deductions and exemptions data"""
        return {
            "zakat": {
                "description": "Zakat paid during the year",
                "limit": "No limit",
                "condition": "Must be paid to eligible recipients"
            },
            "life_insurance": {
                "description": "Life insurance premiums",
                "limit": 500000,
                "condition": "Own life insurance policy"
            },
            "provident_fund": {
                "description": "Provident fund contributions",
                "limit": "As per rules",
                "condition": "Recognized provident fund"
            },
            "medical_expenses": {
                "description": "Medical expenses for disabled dependents",
                "limit": "Actual expenses",
                "condition": "Certified disability"
            },
            "donations": {
                "description": "Donations to approved charitable organizations",
                "limit": "30% of taxable income",
                "condition": "Approved organizations only"
            }
        }
    
    def _get_withholding_rates(self) -> Dict[str, float]:
        """Get withholding tax rates"""
        return {
            "salary": 0,  # Progressive rates apply
            "contract_payment": 10,
            "commission": 10,
            "rent": 10,
            "dividend": 15,
            "bank_interest": 10,
            "prize_bonds": 25,
            "mobile_phone": 10,
            "electricity": 7.5,
            "cash_withdrawal": 0.6
        }
    
    def calculate_income_tax(self, annual_income: float) -> Dict[str, Any]:
        """Calculate income tax based on current slabs"""
        if annual_income <= 0:
            return {
                "total_tax": 0,
                "effective_rate": 0,
                "breakdown": [],
                "net_income": annual_income
            }
        
        total_tax = 0
        breakdown = []
        
        for slab in self.tax_slabs:
            if annual_income <= slab["min_income"]:
                break
            
            taxable_in_slab = min(annual_income, slab["max_income"]) - slab["min_income"] + 1
            if taxable_in_slab > 0:
                tax_in_slab = taxable_in_slab * (slab["rate"] / 100)
                total_tax += tax_in_slab
                
                if tax_in_slab > 0:
                    breakdown.append({
                        "slab": f"Rs. {slab['min_income']:,} - Rs. {slab['max_income']:,}" if slab['max_income'] != float('inf') else f"Above Rs. {slab['min_income']:,}",
                        "rate": slab["rate"],
                        "taxable_amount": taxable_in_slab,
                        "tax": tax_in_slab
                    })
        
        effective_rate = (total_tax / annual_income) * 100 if annual_income > 0 else 0
        net_income = annual_income - total_tax
        
        return {
            "total_tax": total_tax,
            "effective_rate": effective_rate,
            "breakdown": breakdown,
            "net_income": net_income,
            "gross_income": annual_income
        }
    
    def get_tax_slab_info(self) -> str:
        """Get formatted tax slab information"""
        info = f"**Pakistan Income Tax Slabs for Tax Year {self.current_tax_year}:**\n\n"
        
        for slab in self.tax_slabs:
            if slab["max_income"] == float('inf'):
                range_str = f"Above Rs. {slab['min_income']:,}"
            else:
                range_str = f"Rs. {slab['min_income']:,} - Rs. {slab['max_income']:,}"
            
            info += f"• {range_str}: {slab['rate']}%\n"
        
        info += f"\n*Note: These rates are for Tax Year {self.current_tax_year}. Please verify current rates with FBR.*"
        return info
    
    def get_filing_deadlines(self) -> str:
        """Get formatted filing deadlines"""
        info = "**Income Tax Return Filing Deadlines:**\n\n"
        
        for category, deadline in self.important_dates.items():
            category_name = category.replace('_', ' ').title()
            info += f"• {category_name}: {deadline}\n"
        
        info += "\n*Note: Late filing may result in penalties. File through FBR's IRIS portal.*"
        return info
    
    def get_deductions_info(self) -> str:
        """Get formatted deductions information"""
        info = "**Common Tax Deductions and Exemptions:**\n\n"
        
        for deduction, details in self.deductions.items():
            name = deduction.replace('_', ' ').title()
            limit_str = f"Rs. {details['limit']:,}" if isinstance(details['limit'], (int, float)) else details['limit']
            
            info += f"• **{name}**: {details['description']}\n"
            info += f"  - Limit: {limit_str}\n"
            info += f"  - Condition: {details['condition']}\n\n"
        
        info += "*Note: Consult current tax laws for detailed eligibility criteria.*"
        return info

# Global instance
pakistan_tax_data = PakistanTaxData()

def get_tax_calculation(income: float) -> Dict[str, Any]:
    """Calculate tax for given income"""
    return pakistan_tax_data.calculate_income_tax(income)

def get_tax_slabs() -> str:
    """Get current tax slabs information"""
    return pakistan_tax_data.get_tax_slab_info()

def get_filing_info() -> str:
    """Get filing deadlines information"""
    return pakistan_tax_data.get_filing_deadlines()

def get_deductions() -> str:
    """Get deductions information"""
    return pakistan_tax_data.get_deductions_info()

