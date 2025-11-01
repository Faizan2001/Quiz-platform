# Developer Questions – Client Responses

---

## Functionality & Quiz Flow

1. **Can users resume a quiz if they exit midway?**  
   - Not in Phase 1. Later, they can save the state and reopen the quiz.

2. **Should questions appear in random order or fixed order?**  
   - Randomly chosen before the quiz starts. Presentation order doesn’t matter.

3. **Can users retake the same quiz, or only attempt it once?**  
   - Each quiz should differ; questions are randomly selected from the pool each time.

4. **Should quizzes have a time limit per quiz or per question?**  
   - Per quiz.

5. **After submitting, should users see correct answers or just their score?**  
   - Show incorrect answers, correct answers for those, and total score.

6. **Can quizzes include images, equations, or multimedia content?**  
   - Not initially. Later, a separate module will allow line drawing over sketches or pictures.

---

## User Roles & Access

7. **Will there be multiple organizations using the same system (multi-tenant)?**  
   - Single-tenant.

8. **Can a user belong to more than one organization?**  
   - Not relevant.

9. **Should Org Admins only manage users within their organization?**  
   - Not relevant.

10. **Can a Quiz Admin also take quizzes as a normal user?**  
    - Yes, same as any other user.

---

## Question Uploads & Management

11. **Will you provide a sample CSV/XLSX format for question uploads?**  
    - Yes, after the ER diagram is finalized.

12. **Should uploads replace existing questions or only add new ones?**  
    - Questions are uploaded into the pool and remain until deleted by a Quiz Admin.

13. **Should there be a question approval/review process before they go live?**  
    - No.

---

## Results & Reporting

14. **Should results show detailed breakdowns per question or just final scores?**  
    - Show score, incorrect answers, and correct answers for those.

15. **Should admins have access to reports by user, category, or quiz?**  
    - Reports not necessary; on-screen viewing is sufficient.

16. **Do users need to see their past attempts and scores in history?**  
    - No.

---

## Subscription & Payments

17. **What payment gateway should be used?**  
    - Stripe.

18. **Will subscriptions renew automatically or require manual renewal?**  
    - Manual.

19. **Should user access be restricted when a subscription expires?**  
    - Yes, access stops.

---

## Technical & Deployment

20. **Who will host the platform — your team or ours?**  
    - Our team. We will own copyright of all developed and documented materials.

21. **Do you have a preferred hosting provider? (Render, Railway, DigitalOcean, etc.)**  
    - Not specified; “don’t worry about that.”

22. **Should backups and logs be automated or manual?**  
    - We will back up the database and app separately.

---

## UI & Design

23. **Do you have reference design, theme, or branding guidelines?**  
    - No reference design yet; a tentative layout will be provided. Branding options should be available.

24. **Should the quiz interface be fully mobile-responsive in Phase 1?**  
    - No.

25. **Should we include a progress bar or “Question X of Y” indicator?**  
    - Not necessary.

---

## Data & Configuration

26. **Will each organization have unique configuration settings (logo, name, contact info)?**  
    - Only one organization setup.

27. **Should configurations be editable by Org Admins or only developers?**  
    - Org Admins.

---

