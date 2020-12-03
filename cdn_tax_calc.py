# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 23:54:21 2020

@author: Thadchayani K
"""

class incomeTax: 
    def incomeInput(self):
        self.emp_income = None
        self.se_income = None
        self.o_income = None
        self.e_div = None
        self.i_div = None
        self.c_g = None
        self.taxPaid = None
        self.rrsp = None
        
        while self.emp_income is None:
            try:
                self.emp_income = float(input('What is your employment income? '))
            except ValueError:
                print ("Input not valid!")
                
        while self.se_income is None:
            try:
                self.se_income = float(input('What is your self-employment income? '))
            except ValueError:
                print ("Input not valid!")
                
        while self.o_income is None:
            try:
                self.o_income = float(input('Do you have any other income (EI, CPP & etc.)? (Input 0 if no) '))
            except ValueError:
                print ("Input not valid!")
                
        while self.e_div is None:
            try:
                self.e_div = float(input('Do you have any eligible dividends? (These are dividends from public companies, Input 0 if no) '))
            except ValueError:
                print ("Input not valid!")
                
        while self.i_div is None:
            try:
                self.i_div = float(input('Do you have any ineligible dividends? (These are dividends from private companies, Input 0 if no) '))
            except ValueError:
                print ("Input not valid!")
        
        while self.c_g is None:
            try:
                self.c_g = float(input('Do you have any capital gains? (Input 0 if no) '))
            except ValueError:
                print ("Input not valid!")
                
        while self.taxPaid is None:
            try:
                self.taxPaid = float(input('Input the amount of income tax you have paid (ex. tax deducted from your paycheque [not including CPP/EI]): '))
            except ValueError:
                print ("Input not valid!")
                
        while self.rrsp is None:
            try:
                self.rrsp = float(input('Enter RRSP deduction: '))
            except ValueError:
                print ("Input not valid!")
                
        self.a_income = self.emp_income + self.o_income
        self.salary = self.a_income + self.se_income + self.c_g + self.e_div + self.i_div
        return(self.salary)

    def taxableDiv(self):
        self.taxable_e_div = self.e_div * 1.38
        self.taxable_i_div = self.i_div * 1.15
    
    def CPP(self,province):
        cpp_max = 57400
        cpp_exemp = 3500
        if province.lower() == 'qc':
            cppqpp = 0.111
        else:
            cppqpp = 0.102
        self.total_inc = self.emp_income + self.se_income
        self.emp_cpp = (max(0,min(self.emp_income, cpp_max) - cpp_exemp)*cppqpp)/2
        self.se_cpp = 0
        
        if self.se_income == 0:
            return(self.emp_cpp)
        
        if (self.se_income > 0 and self.emp_income == 0):
            self.se_cpp = max(0, min(self.se_income, cpp_max) - cpp_exemp) * cppqpp
            return (self.se_cpp)
        
        elif (self.se_income > 0 and self.emp_income > 0):
            self.se_cpp = max(0, min(self.total_inc, cpp_max) - cpp_exemp) * cppqpp
            self.se_cpp = self.se_cpp - (self.emp_cpp * 2)
            return(self.se_cpp)
        
    def EI(self):
        ei_max = 53100
        ei_rate = 0.0162
        self.ei_premiums = max(0, min(self.emp_income, ei_max)) * ei_rate
        return(self.ei_premiums)
    
    def payRollDeductions(self):
        self.payroll_d = self.emp_cpp + self.ei_premiums
        return(self.payroll_d)
    
    def payRollTaxCred(self):
        self.payroll_tc = self.emp_cpp + (self.se_cpp/2) + self.ei_premiums
        return(self.payroll_tc)
    
    def taxableIncome(self):
        self.income = self.a_income + self.se_income + self.taxable_e_div + self.taxable_i_div + (self.c_g / 2) - self.rrsp - (self.se_cpp/2)
        return (self.income) 

    def taxBracket(self, salary, province):
        self.ftax = 0
        self.ptax = 0
        self.can_emp_amt = min(1222,self.emp_income + self.se_income)
        
        if self.income <= 47630:
            self.ftax = self.income * 0.15;
        elif self.income <= 95259:
            self.ftax = (self.income - 47630) * 0.205 + 7145;
        elif self.income <= 147667:
            self.ftax = (self.income - 95259) * 0.26 + 16908;
        elif self.income <= 210371:
            self.ftax = (self.income - 147667) * 0.29 + 30535
        else:
            self.ftax = (self.income - 210371) * 0.33 + 48719
        
        self.ftax = max(self.ftax - ((12069 + self.can_emp_amt + self.payroll_tc) * 0.15), 0)
        self.ftax = max(self.ftax - (self.taxable_e_div * 0.150198) - (self.taxable_i_div * 0.090301), 0)
        
        if province.lower() == 'qc':
            self.ftax = self.ftax * 0.835
        
        if province.lower() == 'on':
            if self.income <= 43906:
                self.ptax = self.income * 0.0505
            elif self.income <= 87813:
                self.ptax = 2217.25 + ((self.income - 43906) * 0.0915)
            elif self.income <= 150000:
                self.ptax = 6234.74 + ((self.income - 87813) * 0.1116)
            elif self.income <= 220000:
                self.ptax = 13174.80 + ((self.income - 150000) * 0.1216)
            else:
                self.ptax = 21686.8 + ((self.income - 220000) * 0.1316)
            self.ptax = max(self.ptax - ((10582 + self.payroll_tc) * 0.0505), 0)
        
        if province.lower() == 'qc':
            if self.income <= 43790:
                self.ptax = self.income * 0.15
            elif self.income <= 87575:
                self.income = 6568.5 + ((salary - 43790) * 0.20)
            elif self.income <= 106555:
                self.ptax = 15325.5 + ((self.income-87575) * 0.24)
            else:
                self.ptax = 19880.7 + ((self.income - 106555) * 0.2575)
            self.ptax = max(self.ptax - (15269 * 0.15), 0)
            self.ptax = max(self.ptax - (self.taxable_e_div * 0.1178) - (self.taxable_i_div * 0.0555), 0)
        
        self.tax = self.ftax + self.ptax + self.payroll_d + self.se_cpp
        return(self.tax)
        
    def RRSP(self):
        if (self.rrsp > 0):
            self.rrspTax = self.rrsp - self.tax
            self.rrspD = self.tax - self.rrspTax
            return(abs(self.rrspD))
        else:
            return(0)
    
    def refund(self):
        self.refund = self.taxPaid - (self.ftax + self.ptax + self.se_cpp)
        if self.refund >= 0:
            print("Tax Refund: ", '${:,.2f}'.format(abs(self.refund)))
        else:
            print("Tax Owing: ", '${:,.2f}'.format(abs(self.refund)))
    
def main():
    it = incomeTax()
    print('Welcome to using this tax calculator.')
    print('The taxes calculated in this app in terms of provinces only contain ontario and quebec.')
    print('DISCLAIMER: DO NOT ACTUALLY USE THIS FOR YOUR TAXES!')
    print('**************************************************************')
    name = str(input('What is your name? '))
    province = str(input('What province are you from? ON or QC? '))
    totalIncome = it.incomeInput()
    taxableDiv = it.taxableDiv()
    cpp = it.CPP(province)
    ei_premium = it.EI()
    payRollD = it.payRollDeductions()
    payrollTC = it.payRollTaxCred()
    taxableIncome = it.taxableIncome()
    totalTax = it.taxBracket(totalIncome, province)
    rrsp = it.RRSP()
    print('Now calculating your taxes...')
    print('-----------------------------------------------------------------')
    print('Hi ' + name + ',')
    print('Here are your tax return details:')
    print('**************************************************************')
    print('Your total income:', '${:,.2f}'.format(totalIncome))
    print('Your total income after taxes:', '${:,.2f}'.format((totalIncome-totalTax)))
    print('Your total Taxes: ', '${:,.2f}'.format(totalTax))
    print('Your taxable income: ', '${:,.2f}'.format(taxableIncome))
    print('Your taxable ELIGIBLE dividends: ', '${:,.2f}'.format(it.taxable_e_div))
    print('Your taxable INELIGIBLE dividends: ', '${:,.2f}'.format(it.taxable_i_div))
    print('Your federal tax amount: ', '${:,.2f}'.format(it.ftax))
    print('Your provincial tax amount (' + province + '): ', '${:,.2f}'.format(it.ptax))
    print('**************************************************************')
    print('CPP Premium (Employment): ', '${:,.2f}'.format(it.emp_cpp))
    print('CPP Premium (Self Employment: ', '${:,.2f}'.format(it.se_cpp))
    print('EI Premiums: ', '${:,.2f}'.format(ei_premium))
    print('Your payroll deductions: ', '${:,.2f}'.format(payRollD))
    print('Your payroll tax credit: ', '${:,.2f}'.format(payrollTC))
    print('Your RRSP savings: ', '${:,.2f}'.format(rrsp))
    print('**************************************************************')
    taxReturn = it.refund()
    #print('The tax owed on $', income, 'after standard deduction is $', round(totalTax,2), 'and your net income after tax is $', round((income-totalTax),2))               
main()