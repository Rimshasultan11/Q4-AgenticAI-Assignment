import rich
from connection import config
import asyncio
from pydantic import BaseModel
from agents import Agent, RunContextWrapper,function_tool,Runner


# bank_account = BankAccount(
#     account_number="ACC-789456",
#     customer_name="Fatima Khan",
#     account_balance=75500.50,
#     account_type="savings"
# )



class BankAccount(BaseModel):
    account_number: int | str
    customer_name: str
    account_balance: float
    account_type: str



   
bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Rimsha Khan",
    account_balance=75500.50,
    account_type="savings"
)



@function_tool
def get_bank_account_details(wrapper:RunContextWrapper[BankAccount]):
    return f'the bank account details are: {wrapper.context}'

bank_account_agent = Agent(
    name="bank_account_agent",
    instructions= "You are a helpful assistant, always call the tool to get the bank account details.",
    tools=[get_bank_account_details],
)

# 2. STUDENT PROFILE CONTEXT

# student = StudentProfile(
#     student_id="STU-456",
#     student_name="Hassan Ahmed",
#     current_semester=4,
#     total_courses=5
# )

class StudentProfile(BaseModel):
    student_id: int | str
    student_name: str
    current_semester: int
    total_courses: int


student_profile = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

@function_tool
def get_student_profile(wrapper:RunContextWrapper[StudentProfile]):
    return f'the student profile details are: {wrapper.context}'

student_profile_agent = Agent(
    name="student_profile_agent",
    instructions= "You are a helpful assistant, always call the tool to get the student profile details.",
    tools=[get_student_profile],
)

# 3. LIBRARY BOOK CONTEXT
# library_book = LibraryBook(
#     book_id="BOOK-123",
#     book_title="Python Programming",
#     author_name="John Smith",
#     is_available=True
# )

class LibraryBook(BaseModel):
    book_id: int | str
    book_title: str
    author_name: str
    is_available: bool

library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)

@function_tool
def get_library_book(wrapper:RunContextWrapper[LibraryBook]):
    return f'the library book details are: {wrapper.context}'

library_book_agent = Agent(
    name="library_book_agent",
    instructions= "You are a helpful assistant, always call the tool to get the library book details.",
    tools=[get_library_book],
)


async def main():
    # bank accoubt runner
    bank_result = await Runner.run(
        bank_account_agent,
        input = "what are the bank account details?" ,
        run_config = config,
        context = bank_account
    )
    rich.print(bank_result.final_output)

    # student profile runner

    student_result = await Runner.run(
        student_profile_agent,
        input = "what are the student profile details?" ,
        run_config = config,
        context = student_profile
    )
    rich.print(student_result.final_output)

    # library book runner
    library_result = await Runner.run(
        library_book_agent,
        input = "what are the library book details?" ,
        run_config = config,
        context = library_book
    )
    rich.print(library_result.final_output)
   

   

if __name__ == "__main__":
    asyncio.run(main())