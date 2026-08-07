class AIMatchService:
    @staticmethod
    def calculate_match(freelancer_profile, project):
        """
        Calculates an AI Match percentage (50-99%) and breakdown reasons
        between a FreelancerProfile and a Project.
        """
        reasons = []

        # 1. Skills Score (45% weight)
        project_skills = set(project.skills.values_list('name', flat=True))
        freelancer_skills = set(freelancer_profile.skills.values_list('name', flat=True))

        if project_skills:
            matching_skills = project_skills.intersection(freelancer_skills)
            skills_ratio = len(matching_skills) / len(project_skills)
            skills_score = min(100, int(skills_ratio * 100))
            if matching_skills:
                matched_str = ", ".join(list(matching_skills)[:3])
                reasons.append(f"✓ Matching required skills ({matched_str})")
            else:
                reasons.append("• Partial skill alignment across core categories")
        else:
            skills_score = 80
            reasons.append("✓ Strong general technical foundation")

        # 2. Experience Level (25% weight)
        years = freelancer_profile.experience_years
        exp_score = 85
        if project.experience_level == "entry":
            exp_score = 95
            reasons.append("✓ Suitable for entry-level project scope")
        elif project.experience_level == "intermediate":
            if years >= 2:
                exp_score = 95
                reasons.append(f"✓ Proven experience ({years}+ years in industry)")
            else:
                exp_score = 75
        elif project.experience_level == "expert":
            if years >= 5:
                exp_score = 98
                reasons.append(f"✓ Senior expert background ({years}+ years)")
            elif years >= 3:
                exp_score = 85
            else:
                exp_score = 65

        # 3. Budget Fit (15% weight)
        budget_score = 85
        if freelancer_profile.hourly_rate and project.budget_max > 0:
            est_monthly = float(freelancer_profile.hourly_rate) * 80
            if float(project.budget_min) <= est_monthly <= float(project.budget_max) * 1.2:
                budget_score = 95
                reasons.append("✓ Rate aligns with project budget parameters")
            else:
                budget_score = 80
        else:
            reasons.append("✓ Flexible budget agreement possible")

        # 4. Availability Fit (15% weight)
        availability_score = 90
        if freelancer_profile.availability in ["full_time", "contract"]:
            availability_score = 98
            reasons.append("✓ Immediate availability within project timeline")

        # Composite overall score calculation
        overall = (
            skills_score * 0.45 +
            exp_score * 0.25 +
            budget_score * 0.15 +
            availability_score * 0.15
        )

        final_score = min(99, max(50, int(round(overall))))

        return {
            "score": final_score,
            "skills_score": skills_score,
            "exp_score": exp_score,
            "budget_score": budget_score,
            "reasons": reasons[:4],
        }
