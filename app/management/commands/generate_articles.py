import os
import random
import urllib.request
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from app.models import Article, Category


class Command(BaseCommand):
    help = 'Generate mock articles with images for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            ('Community Events', 'community-events'),
            ('Success Stories', 'success-stories'),
            ('Health & Wellness', 'health-wellness'),
            ('Education', 'education'),
            ('Volunteer Spotlight', 'volunteer-spotlight'),
        ]
        
        categories = []
        for name, slug in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'  Created category: {name}')
            else:
                self.stdout.write(f'  Category exists: {name}')
        
        # Get or create an admin user as author
        author = User.objects.filter(is_staff=True).first()
        if not author:
            author = User.objects.first()
        if not author:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return
        
        self.stdout.write(f'\nUsing author: {author.username}')
        self.stdout.write('\nCreating articles...\n')
        
        # Article data
        articles_data = [
            {
                'title': 'Annual Community Cleanup Day Brings Together 500 Volunteers',
                'excerpt': 'Our biggest cleanup event yet saw volunteers from all walks of life unite to beautify local parks and neighborhoods.',
                'content': '''
                <h2>A Day of Unity and Action</h2>
                <p>Last Saturday marked our most successful Community Cleanup Day in the history of the HappyNess Project. Over 500 volunteers gathered at dawn, armed with gloves, trash bags, and an unstoppable spirit of community service.</p>
                
                <p>The event covered 15 different locations across the city, including three major parks, two school playgrounds, and several neighborhood streets that had been neglected for years.</p>
                
                <h3>The Impact</h3>
                <p>By the end of the day, our incredible volunteers had collected:</p>
                <ul>
                    <li>Over 2,000 pounds of trash and debris</li>
                    <li>500+ recyclable items properly sorted</li>
                    <li>Planted 50 new trees in local parks</li>
                    <li>Repainted 3 community centers</li>
                </ul>
                
                <blockquote>"This is what community looks like. People coming together, not because they have to, but because they want to make a difference." - Maria Santos, Volunteer Coordinator</blockquote>
                
                <h3>Looking Forward</h3>
                <p>The success of this event has inspired us to make it a quarterly occurrence. We're already planning the next cleanup for spring, with even bigger goals in mind.</p>
                
                <p>Thank you to everyone who participated, donated supplies, or simply spread the word. Together, we're building a happier, healthier community.</p>
                ''',
                'category': 'community-events',
                'is_featured': True,
            },
            {
                'title': 'From Homeless to Homeowner: Sarah\'s Inspiring Journey',
                'excerpt': 'After three years in our housing program, Sarah has achieved what once seemed impossible - owning her own home.',
                'content': '''
                <h2>A Story of Resilience</h2>
                <p>Sarah Thompson never imagined she would own a home. Just five years ago, she was living in her car with her two young children, working two minimum-wage jobs, and struggling to see a way forward.</p>
                
                <p>"I remember the day I walked into the HappyNess Project office," Sarah recalls. "I was embarrassed, scared, and had almost given up hope. But the team there didn't judge me. They saw me as a person with potential."</p>
                
                <h3>The Transformation</h3>
                <p>Through our comprehensive support program, Sarah received:</p>
                <ul>
                    <li>Emergency housing assistance</li>
                    <li>Job training and career counseling</li>
                    <li>Financial literacy workshops</li>
                    <li>Childcare support while she attended classes</li>
                    <li>Mental health counseling</li>
                </ul>
                
                <p>Within 18 months, Sarah had secured a stable job as a medical assistant. She started saving money and building her credit score.</p>
                
                <h3>The Dream Realized</h3>
                <p>Last month, Sarah closed on a three-bedroom home in a safe neighborhood with excellent schools. Her children, now 8 and 10, each have their own room for the first time in their lives.</p>
                
                <blockquote>"The HappyNess Project didn't just give me a handout. They gave me the tools to build a life. I'm proof that with the right support, anyone can overcome their circumstances."</blockquote>
                
                <p>Sarah now volunteers with our organization, mentoring other single mothers on their journey to stability.</p>
                ''',
                'category': 'success-stories',
                'is_featured': False,
            },
            {
                'title': 'New Mental Health Initiative Launches This Month',
                'excerpt': 'We\'re expanding our services to include free counseling sessions and mental health workshops for community members.',
                'content': '''
                <h2>Prioritizing Mental Wellness</h2>
                <p>Mental health is health. That's the message behind our new initiative launching this month, designed to bring accessible mental health resources to every member of our community.</p>
                
                <h3>What We're Offering</h3>
                <p>Our comprehensive mental health program includes:</p>
                <ul>
                    <li><strong>Free Individual Counseling:</strong> Up to 10 sessions per person with licensed therapists</li>
                    <li><strong>Support Groups:</strong> Weekly meetings for various concerns including grief, anxiety, and life transitions</li>
                    <li><strong>Wellness Workshops:</strong> Monthly sessions on stress management, mindfulness, and emotional resilience</li>
                    <li><strong>Crisis Hotline:</strong> 24/7 support for those in immediate need</li>
                </ul>
                
                <h3>Breaking the Stigma</h3>
                <p>One of our primary goals is to normalize conversations about mental health. Too many people suffer in silence because they're afraid of being judged.</p>
                
                <p>"We want everyone to know that seeking help is a sign of strength, not weakness," says Dr. James Chen, our program director. "Mental health challenges can affect anyone, and there's no shame in needing support."</p>
                
                <h3>How to Access Services</h3>
                <p>All services are free and confidential. To schedule an appointment or learn more, visit our wellness center or call our main office. Walk-ins are also welcome.</p>
                ''',
                'category': 'health-wellness',
                'is_featured': False,
            },
            {
                'title': 'Youth Coding Bootcamp Graduates 30 Students',
                'excerpt': 'Our free 12-week coding program has produced another successful cohort, with several students already landing internships.',
                'content': '''
                <h2>Building Tomorrow's Tech Leaders</h2>
                <p>Last Friday evening, we celebrated the graduation of 30 talented young people from our Youth Coding Bootcamp. These students, aged 14-19, completed an intensive 12-week program learning web development, programming fundamentals, and professional skills.</p>
                
                <h3>The Curriculum</h3>
                <p>Students learned a comprehensive stack of technologies:</p>
                <ul>
                    <li>HTML, CSS, and JavaScript fundamentals</li>
                    <li>React.js for frontend development</li>
                    <li>Python for backend programming</li>
                    <li>Database design and management</li>
                    <li>Version control with Git</li>
                    <li>Professional communication and teamwork</li>
                </ul>
                
                <h3>Real-World Projects</h3>
                <p>Each student completed a capstone project addressing a real community need. Projects included:</p>
                <ul>
                    <li>A neighborhood resource finder app</li>
                    <li>A volunteer coordination platform</li>
                    <li>An educational game for elementary students</li>
                    <li>A local business directory supporting minority-owned shops</li>
                </ul>
                
                <blockquote>"I never thought I could be a programmer. This bootcamp showed me that with dedication and the right teachers, anything is possible." - Marcus, 17, Graduate</blockquote>
                
                <h3>What's Next</h3>
                <p>Applications for our next cohort open next month. The program is completely free, including laptop loans for students who need them.</p>
                ''',
                'category': 'education',
                'is_featured': False,
            },
            {
                'title': 'Meet Our Volunteer of the Month: James Rodriguez',
                'excerpt': 'James has dedicated over 1,000 hours to our food bank program, helping feed hundreds of families each month.',
                'content': '''
                <h2>A Heart for Service</h2>
                <p>Every Tuesday and Thursday morning, before the sun rises, James Rodriguez is already at our community food bank. He's been doing this for three years straight, rain or shine, never missing a shift.</p>
                
                <p>"I know what it's like to be hungry," James shares. "When I was a kid, my family relied on food assistance. Now that I'm in a position to give back, I can't imagine doing anything else."</p>
                
                <h3>The Impact</h3>
                <p>James doesn't just sort and distribute food. He's become a leader in our volunteer community:</p>
                <ul>
                    <li>Trained over 50 new volunteers</li>
                    <li>Implemented a new inventory system that reduced waste by 30%</li>
                    <li>Started a "personal shopper" program for elderly and disabled clients</li>
                    <li>Organized monthly nutrition workshops</li>
                </ul>
                
                <h3>Beyond the Numbers</h3>
                <p>What makes James special isn't just the hours he puts in—it's the way he connects with every person who comes through our doors.</p>
                
                <blockquote>"James remembers everyone's name, their kids' names, what they like to cook. He makes people feel seen and valued, not just like they're receiving charity." - Food Bank Director, Angela Martinez</blockquote>
                
                <p>When asked about his motivation, James smiles: "I get more out of this than I give. Every smile, every thank you—that's my reward."</p>
                ''',
                'category': 'volunteer-spotlight',
                'is_featured': False,
            },
            {
                'title': 'Summer Reading Program Kicks Off With Record Enrollment',
                'excerpt': 'Over 200 children have signed up for our summer literacy initiative, surpassing last year\'s numbers by 40%.',
                'content': '''
                <h2>Reading Adventures Await</h2>
                <p>Summer break doesn't mean learning takes a vacation! Our annual Summer Reading Program launched this week with unprecedented enthusiasm, as over 200 children ages 5-12 signed up to participate.</p>
                
                <h3>Program Highlights</h3>
                <p>This year's theme is "Around the World in 80 Books," taking young readers on a literary journey across cultures and continents:</p>
                <ul>
                    <li>Weekly reading challenges with prizes</li>
                    <li>Author video chats featuring diverse writers</li>
                    <li>Cultural craft activities connected to featured books</li>
                    <li>Free books to keep—because every child deserves a home library</li>
                    <li>End-of-summer celebration party</li>
                </ul>
                
                <h3>Why It Matters</h3>
                <p>Research shows that children who don't read during summer can lose up to two months of academic progress—a phenomenon known as "summer slide." Our program keeps young minds active and engaged.</p>
                
                <p>"We've seen children who started as reluctant readers become book enthusiasts," says program coordinator Lisa Park. "The key is making reading fun and social."</p>
                
                <h3>Join the Adventure</h3>
                <p>Registration remains open throughout June. All materials are provided free of charge, including a reading log, bookmarks, and a starter book pack.</p>
                ''',
                'category': 'education',
                'is_featured': False,
            },
            {
                'title': 'Community Garden Produces 2,000 Pounds of Fresh Vegetables',
                'excerpt': 'Our urban garden initiative is thriving, providing fresh produce to local food pantries and families in need.',
                'content': '''
                <h2>Growing Hope, One Garden at a Time</h2>
                <p>What started as a vacant lot filled with weeds and litter has transformed into a thriving urban oasis. Our Community Garden program just completed its most productive season ever, harvesting over 2,000 pounds of fresh vegetables.</p>
                
                <h3>What We Grew</h3>
                <p>Our volunteer gardeners cultivated a diverse array of produce:</p>
                <ul>
                    <li>500 lbs of tomatoes</li>
                    <li>400 lbs of squash and zucchini</li>
                    <li>300 lbs of peppers</li>
                    <li>250 lbs of leafy greens</li>
                    <li>200 lbs of beans</li>
                    <li>150 lbs of root vegetables</li>
                    <li>200 lbs of herbs and other produce</li>
                </ul>
                
                <h3>Where the Food Goes</h3>
                <p>Half of our harvest is donated directly to local food pantries, ensuring families in need have access to nutritious, fresh produce. The other half goes to participating gardeners—many of whom live in food deserts with limited access to fresh vegetables.</p>
                
                <blockquote>"There's something powerful about growing your own food. It's not just nutrition—it's dignity, connection to the earth, and hope." - Garden Coordinator, Robert Kim</blockquote>
                
                <h3>Get Involved</h3>
                <p>We're accepting plot applications for next season! No experience necessary—we provide training, tools, seeds, and ongoing support.</p>
                ''',
                'category': 'community-events',
                'is_featured': False,
            },
            {
                'title': 'Annual Gala Raises $150,000 for Youth Programs',
                'excerpt': 'Thanks to generous donors, we\'ve secured funding for expanding our after-school and mentorship programs.',
                'content': '''
                <h2>An Evening of Giving and Gratitude</h2>
                <p>The ballroom sparkled with hope and generosity last Saturday as over 300 guests gathered for our Annual Fundraising Gala. By the end of the evening, we had raised an incredible $150,000 for youth programs.</p>
                
                <h3>Highlights of the Evening</h3>
                <p>The gala featured:</p>
                <ul>
                    <li>Keynote address by former program participant, now college graduate, Destiny Williams</li>
                    <li>Live auction with vacation packages, artwork, and exclusive experiences</li>
                    <li>Performance by the HappyNess Youth Choir</li>
                    <li>Silent auction with over 75 donated items</li>
                    <li>Paddle raise that exceeded all expectations</li>
                </ul>
                
                <h3>Where the Funds Will Go</h3>
                <p>The money raised will directly support:</p>
                <ul>
                    <li>Expansion of after-school tutoring to two additional schools</li>
                    <li>Launch of a new mentorship program pairing youth with professionals</li>
                    <li>Summer camp scholarships for 100 children</li>
                    <li>New computers and technology for our learning center</li>
                </ul>
                
                <blockquote>"Every dollar raised tonight represents a child's potential unlocked, a dream made possible. Thank you for believing in our youth." - Executive Director, Patricia Holmes</blockquote>
                
                <p>We extend our heartfelt thanks to all sponsors, donors, and attendees who made this evening a success.</p>
                ''',
                'category': 'community-events',
                'is_featured': False,
            },
            {
                'title': 'Free Health Screenings Serve 400 Community Members',
                'excerpt': 'Our partnership with local healthcare providers brought essential medical services to underserved neighborhoods.',
                'content': '''
                <h2>Healthcare Access for All</h2>
                <p>Last weekend's Community Health Fair was a resounding success, providing free health screenings and services to over 400 community members who might otherwise go without preventive care.</p>
                
                <h3>Services Provided</h3>
                <p>Thanks to our partners at Regional Medical Center and volunteer healthcare professionals, attendees received:</p>
                <ul>
                    <li>Blood pressure and cholesterol screenings</li>
                    <li>Diabetes risk assessments</li>
                    <li>Vision and hearing tests</li>
                    <li>Dental check-ups and cleanings</li>
                    <li>Mental health consultations</li>
                    <li>COVID-19 and flu vaccinations</li>
                    <li>Health education and resources</li>
                </ul>
                
                <h3>Early Detection Saves Lives</h3>
                <p>Several attendees were identified as having previously undiagnosed conditions and were connected with ongoing care. This is exactly why these events matter.</p>
                
                <blockquote>"I hadn't seen a doctor in five years because I couldn't afford it. Today they found something that needed attention. They might have saved my life." - Health Fair Attendee</blockquote>
                
                <h3>Next Steps</h3>
                <p>We're planning quarterly health fairs to continue serving our community. If you're a healthcare professional interested in volunteering, please contact our office.</p>
                ''',
                'category': 'health-wellness',
                'is_featured': False,
            },
            {
                'title': 'Scholarship Program Sends 15 Students to College',
                'excerpt': 'This year\'s scholarship recipients are heading to universities across the country, pursuing dreams of higher education.',
                'content': '''
                <h2>Dreams Take Flight</h2>
                <p>Fifteen exceptional young people from our community are packing their bags for college this fall, thanks to the HappyNess Scholarship Program. These students, who overcame significant obstacles to excel academically, will pursue degrees in fields ranging from nursing to engineering.</p>
                
                <h3>Meet Some of Our Scholars</h3>
                <p><strong>Aisha Johnson</strong> - First in her family to attend college, heading to State University to study pre-med. "I want to come back and serve my community as a doctor."</p>
                
                <p><strong>Miguel Santos</strong> - Overcame homelessness in high school, accepted to Tech Institute for computer science. "HappyNess believed in me when I didn't believe in myself."</p>
                
                <p><strong>Destiny Park</strong> - Single mother of two, pursuing nursing degree. "This scholarship is changing my family's future for generations."</p>
                
                <h3>More Than Money</h3>
                <p>Our scholarship program provides:</p>
                <ul>
                    <li>Full tuition coverage up to $10,000/year</li>
                    <li>Mentorship from successful professionals</li>
                    <li>Summer internship connections</li>
                    <li>Ongoing academic and emotional support</li>
                    <li>Emergency funds for unexpected expenses</li>
                </ul>
                
                <blockquote>"We don't just write checks. We invest in whole people, walking alongside them through their entire college journey."</blockquote>
                
                <p>Applications for next year's scholarships open in January.</p>
                ''',
                'category': 'education',
                'is_featured': False,
            },
            {
                'title': 'Peer Support Group Celebrates 5 Years of Healing',
                'excerpt': 'Our addiction recovery support group marks half a decade of helping community members find sobriety and hope.',
                'content': '''
                <h2>Five Years of Second Chances</h2>
                <p>This week, we celebrated a milestone: five years since our Peer Support Group for addiction recovery held its first meeting. What started with just six people in a small room has grown into a thriving community of healing.</p>
                
                <h3>By the Numbers</h3>
                <p>Over the past five years:</p>
                <ul>
                    <li>Over 500 individuals have participated in our groups</li>
                    <li>Weekly attendance averages 40-50 people</li>
                    <li>85% of regular attendees report sustained recovery</li>
                    <li>30 participants have become certified peer counselors</li>
                    <li>Zero cost to participants—always free</li>
                </ul>
                
                <h3>The Power of Peer Support</h3>
                <p>Unlike traditional treatment models, peer support groups are led by people who have lived experience with addiction and recovery.</p>
                
                <p>"There's something powerful about getting help from someone who's been where you are," explains group facilitator Marcus Thompson, who has been sober for 12 years. "We don't just understand the struggle—we've overcome it."</p>
                
                <blockquote>"This group saved my life. When I walked in, I had lost everything. Now I have my family back, a job I love, and hope for the future." - Anonymous Group Member</blockquote>
                
                <p>Groups meet every Monday and Thursday evening. All are welcome, and anonymity is respected.</p>
                ''',
                'category': 'health-wellness',
                'is_featured': False,
            },
            {
                'title': 'Back-to-School Drive Equips 800 Students',
                'excerpt': 'Community generosity ensured every child in our program started school with the supplies they need to succeed.',
                'content': '''
                <h2>Ready to Learn</h2>
                <p>Thanks to overwhelming community support, our annual Back-to-School Drive was the biggest yet, providing 800 students with backpacks filled with essential school supplies.</p>
                
                <h3>What Each Student Received</h3>
                <p>Every backpack was stocked with:</p>
                <ul>
                    <li>Grade-appropriate notebooks and folders</li>
                    <li>Pens, pencils, and highlighters</li>
                    <li>Calculator (for older students)</li>
                    <li>Art supplies including crayons and colored pencils</li>
                    <li>Ruler, scissors, and glue sticks</li>
                    <li>Personal care items</li>
                </ul>
                
                <h3>Why It Matters</h3>
                <p>For many families, the cost of school supplies is a significant burden. Some parents must choose between buying notebooks and paying utility bills. No child should start the school year at a disadvantage.</p>
                
                <p>"My mom cried when we got home," shared 9-year-old Lily. "She said now she doesn't have to worry about how to get us ready for school."</p>
                
                <h3>Thank You, Donors!</h3>
                <p>This year's drive was supported by:</p>
                <ul>
                    <li>35 local businesses</li>
                    <li>200+ individual donors</li>
                    <li>50 volunteers for sorting and distribution</li>
                </ul>
                
                <blockquote>"When a child has the tools they need, they can focus on what matters: learning and growing." - Program Director</blockquote>
                ''',
                'category': 'community-events',
                'is_featured': False,
            },
            {
                'title': 'Volunteer Training Program Prepares 50 New Helpers',
                'excerpt': 'Our comprehensive training ensures volunteers are equipped to make the greatest impact in their community work.',
                'content': '''
                <h2>Building a Stronger Volunteer Corps</h2>
                <p>Last month, 50 enthusiastic individuals completed our Volunteer Training Program, ready to serve across all HappyNess Project initiatives. This diverse group brings skills, passion, and fresh energy to our mission.</p>
                
                <h3>Training Curriculum</h3>
                <p>Our 20-hour training program covers:</p>
                <ul>
                    <li>Organization history, mission, and values</li>
                    <li>Understanding the communities we serve</li>
                    <li>Trauma-informed approaches to service</li>
                    <li>Cultural competency and inclusion</li>
                    <li>Boundaries and self-care for volunteers</li>
                    <li>Practical skills for specific volunteer roles</li>
                </ul>
                
                <h3>Diverse Backgrounds, Unified Purpose</h3>
                <p>This cohort includes:</p>
                <ul>
                    <li>Retired teachers and healthcare workers</li>
                    <li>College students seeking experience</li>
                    <li>Corporate professionals donating skills</li>
                    <li>Former program participants giving back</li>
                    <li>Families volunteering together</li>
                </ul>
                
                <blockquote>"I retired last year and felt lost. This training gave me purpose again. I can't wait to start serving." - New Volunteer, Gloria, age 67</blockquote>
                
                <h3>Join Our Team</h3>
                <p>The next volunteer training session begins next month. No experience necessary—just a heart for service.</p>
                ''',
                'category': 'volunteer-spotlight',
                'is_featured': False,
            },
            {
                'title': 'Art Therapy Program Helps Trauma Survivors Heal',
                'excerpt': 'Creative expression becomes a pathway to recovery for community members processing difficult experiences.',
                'content': '''
                <h2>Healing Through Creativity</h2>
                <p>Words aren't always enough to express pain. That's why our new Art Therapy Program has become a vital resource for community members working through trauma, grief, and mental health challenges.</p>
                
                <h3>About the Program</h3>
                <p>Led by licensed art therapists, participants explore healing through:</p>
                <ul>
                    <li>Painting and drawing</li>
                    <li>Sculpture and clay work</li>
                    <li>Collage and mixed media</li>
                    <li>Journaling and creative writing</li>
                    <li>Movement and music integration</li>
                </ul>
                
                <h3>The Science of Art Therapy</h3>
                <p>Art therapy isn't just about making pretty pictures. It's an evidence-based practice that helps people:</p>
                <ul>
                    <li>Process emotions that are hard to verbalize</li>
                    <li>Reduce anxiety and stress</li>
                    <li>Improve self-esteem and self-awareness</li>
                    <li>Develop healthy coping mechanisms</li>
                    <li>Build connections with others in group settings</li>
                </ul>
                
                <blockquote>"I couldn't talk about what happened to me. But I could paint it. And somehow, that started my healing." - Program Participant</blockquote>
                
                <h3>Sessions Available</h3>
                <p>We offer both individual and group sessions, with special programming for children, teens, adults, and seniors. All materials are provided free of charge.</p>
                ''',
                'category': 'health-wellness',
                'is_featured': False,
            },
            {
                'title': 'Partnership with Local Businesses Creates 100 Jobs',
                'excerpt': 'Our employment initiative connects trained community members with local employers seeking dedicated workers.',
                'content': '''
                <h2>Opening Doors to Opportunity</h2>
                <p>We're thrilled to announce that our Workforce Development Partnership has now placed 100 community members in stable employment with local businesses. This milestone represents transformed lives and strengthened families.</p>
                
                <h3>How the Program Works</h3>
                <p>Our comprehensive approach includes:</p>
                <ul>
                    <li>Skills assessment and career counseling</li>
                    <li>Job-specific training and certifications</li>
                    <li>Resume writing and interview preparation</li>
                    <li>Direct connections with hiring employers</li>
                    <li>Ongoing support after placement</li>
                </ul>
                
                <h3>Employer Partners</h3>
                <p>We work with businesses across sectors who value diverse, motivated employees:</p>
                <ul>
                    <li>Healthcare facilities</li>
                    <li>Manufacturing companies</li>
                    <li>Retail and hospitality</li>
                    <li>Construction and trades</li>
                    <li>Technology startups</li>
                </ul>
                
                <blockquote>"The candidates from HappyNess Project are some of our best hires. They're motivated, trained, and grateful for the opportunity." - HR Director, Partner Company</blockquote>
                
                <h3>Success Story</h3>
                <p>David was unemployed for two years after a workplace injury. Through our program, he received retraining, interview coaching, and was placed with a manufacturing company. Six months later, he was promoted to team lead.</p>
                
                <p>"I thought my working days were over. HappyNess showed me I had value."</p>
                ''',
                'category': 'success-stories',
                'is_featured': False,
            },
        ]
        
        # Unsplash image URLs (these are direct links to images that work for demo)
        image_topics = [
            'community,people,volunteers',
            'home,family,happy',
            'mental-health,wellness,calm',
            'coding,students,learning',
            'volunteer,helping,kindness',
            'reading,children,books',
            'garden,vegetables,nature',
            'gala,celebration,event',
            'health,medical,doctor',
            'graduation,students,college',
            'support,group,healing',
            'school,backpack,supplies',
            'training,team,learning',
            'art,therapy,creative',
            'job,work,employment',
        ]
        
        created_count = 0
        for i, article_data in enumerate(articles_data):
            slug = slugify(article_data['title'])
            
            # Check if article already exists
            if Article.objects.filter(slug=slug).exists():
                self.stdout.write(f'  Skipped (exists): {article_data["title"][:50]}...')
                continue
            
            # Get category
            category = Category.objects.get(slug=article_data['category'])
            
            # Create article
            article = Article(
                title=article_data['title'],
                slug=slug,
                excerpt=article_data['excerpt'],
                content=article_data['content'],
                category=category,
                author=author,
                status='published',
                is_featured=article_data.get('is_featured', False),
                published_at=timezone.now() - timezone.timedelta(days=random.randint(1, 60)),
            )
            
            # Download and attach image
            try:
                topic = image_topics[i % len(image_topics)]
                # Using picsum.photos for reliable placeholder images
                image_url = f'https://picsum.photos/seed/{slug[:20]}/1200/630'
                
                self.stdout.write(f'  Downloading image for: {article_data["title"][:40]}...')
                
                req = urllib.request.Request(
                    image_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response = urllib.request.urlopen(req, timeout=10)
                image_data = response.read()
                
                # Save image to article
                image_name = f'{slug[:50]}.jpg'
                article.featured_image.save(image_name, ContentFile(image_data), save=False)
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'    Could not download image: {e}'))
            
            article.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'  Created: {article_data["title"][:50]}...'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done! Created {created_count} articles.'))
        self.stdout.write(f'Total articles in database: {Article.objects.count()}')
        self.stdout.write(f'Published articles: {Article.objects.filter(status="published").count()}')
