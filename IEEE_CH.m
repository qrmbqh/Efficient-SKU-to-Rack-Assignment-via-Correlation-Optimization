function racks = IEEE_CH(data, midu)
tic;
C = zeros(size(data,2), size(data,2));
for i = 1:size(data,2)
    for j = i+1:size(data,2)
        count = sum(sum(data(:,[i,j]),2) == 2);
        C(i,j) = count;
        C(j,i) = count;
    end
end
%Step1:
[~,U] = sort(sum(data),'descend');
best = -1;
for m = 1:size(U,2)
%Step2:
    if m == 1
        L = U;
    else 
        L = [U(m:end),U(1:m-1)];
    end
    C2 = C;
    A = zeros(size(U,2),ceil(size(U,2)/midu)); 
    centers = zeros(1, size(U,2));
    center_step = 1;
    assigned_skus = zeros(1,size(U,2));
    assigned_step = 1;
    for i = 1:floor(size(U,2)/midu)
        remain_skus = L(~ismember(L,assigned_skus));
        center = remain_skus(1);
        centers(center_step) = center;
        assigned_skus(assigned_step) = center;
        center_step = center_step + 1;
        assigned_step = assigned_step + 1;
        A(center, i) = 1;
        [~,candicates] = sort(C(center,:),'descend');
        temp = candicates(~ismember(candicates, assigned_skus));
        chosen_skus = temp(1:midu-1);
        assigned_skus(assigned_step:assigned_step+midu-2) = chosen_skus;
        assigned_step = assigned_step + midu-1;
        A(chosen_skus, i) = 1;
    end
    if assigned_step ~= size(U,2) + 1
        temp = L(~ismember(L,assigned_skus));
        center = temp(1);
        centers(center_step) = center;
        center_step = center_step + 1;
        A(temp, end) = 1;
    end
    %Step3:
    values = zeros(1,ceil(size(U,2)/midu));
    for i = 1:size(A,2)
        center = centers(i);
        members = find(A(:,i)).';
        value = sum(C(center,members));
        values(i) = value;
    end
    [~,rack_idx] = sort(values, 'descend');
    tabu = centers;
    tabu_step = center_step;
    for i = 1:size(rack_idx,2)-1
        for j = i+1:size(rack_idx,2)
            rack1 = rack_idx(i);
            center1 = centers(rack1);
            rack2 = rack_idx(j);
            center2 = centers(rack2);
            rack1_skus = find(A(:,rack1)).';
            rack2_skus = find(A(:,rack2)).';
            for k = 1:size(rack1_skus,2)
                for l = 1:size(rack2_skus,2)
                    sku1 = rack1_skus(k);
                    sku2 = rack2_skus(l);
                    if and(~ismember(sku1,tabu), ~ismember(sku2,tabu))
                        rack1_skus_temp = rack1_skus;
                        rack2_skus_temp = rack2_skus;
                        rack1_skus_temp(k) = sku2;
                        rack2_skus_temp(l) = sku1;
                        if sum(C(center1,rack1_skus)) + sum(C(center2,rack2_skus)) <= sum(C(center1,rack1_skus_temp)) + sum(C(center2,rack2_skus_temp))
                            A(sku1,rack1) = 0;
                            A(sku1,rack2) = 1;
                            A(sku2,rack2) = 0;
                            A(sku2,rack1) = 1;
                            tabu(tabu_step:tabu_step+1) = [sku1,sku2];
                            tabu_step = tabu_step + 2;
                        end
                    end
                end
            end
        end
    end
    values = zeros(1,ceil(size(U,2)/midu));
    for i = 1:size(A,2)
        center = centers(i);
        members = find(A(:,i)).';
        value = sum(C(center,members));
        values(i) = value;
    end
    if sum(values) > best
        best = sum(values);
        best_A = A;
    end
end
toc;
racks = cell(size(A,2),1);
for i = 1:size(A,2)
        members = find(A(:,i)).';
        racks{i} = members;
end